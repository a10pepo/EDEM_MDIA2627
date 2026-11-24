"""renfe_collector.py - Colector de posiciones de trenes de Renfe y alertas de proximidad.

AVISO: ejercicio universitario. Las alertas son ORIENTATIVAS y NO constituyen un
sistema de seguridad ferroviaria. No deben usarse para tomar decisiones operativas.

Fuente: https://tiempo-real.largorecorrido.renfe.com/renfe-visor/flotaLD.json

Supuestos de diseño:
- `mat` se interpreta como conjunto de matriculas de la unidad fisica. Si dos trenes
  comparten alguna matricula, son el mismo tren fisico con dos servicios consecutivos
  y no se genera alerta entre ellos.
- REGLA DE ALERTA: solo se genera alerta si los dos trenes estan en el mismo tramo A->B
  (mismo codEstAnt y mismo codEstSig, con codEstAnt != codEstSig) Y la distancia es
  estrictamente menor que el umbral. Se asume que los sentidos contrarios circulan por
  vias distintas, asi que dos trenes con A y B invertidos no generan alerta.
- Si codEstAnt == codEstSig el tren parece estar en una estacion y no tiene tramo A->B
  definido: nunca genera alerta.
- `riesgo_mismo_tramo` se conserva en la alerta por compatibilidad con la base de datos;
  con esta regla siempre es verdadero. Las alertas anteriores (regla solo por distancia)
  pueden tener el valor falso.
- `horaLlegadaSigEst` a veces esta en el pasado: se guarda pero no se usa en ninguna regla.
- En modo SAMPLE_FILE no se aplica el filtro de antiguedad (el fichero es estatico).

Configuracion (variables de entorno):
    ALERT_DISTANCE_METERS     umbral de proximidad en metros        (defecto 5000)
    POLL_INTERVAL_SECONDS     pausa entre lecturas, minimo 15       (defecto 30)
    MAX_POSITION_AGE_SECONDS  antiguedad maxima de `time`           (defecto 300)
    RENFE_URL                 URL del recurso JSON
    SAMPLE_FILE               JSON local; si se define, se lee de ahi (sin conexion)
    LOG_LEVEL                 nivel de logging                      (defecto INFO)

Base de datos PostgreSQL (opcional; sin DB_HOST solo se muestra por consola):
    DB_HOST, DB_PORT (5432), DB_NAME (renfe), DB_USER (renfe), DB_PASSWORD
Las posiciones y alertas se guardan en cada ciclo (ver schema.sql). Si la base de datos
falla, se registra un aviso y el colector sigue; reintenta la conexion en el ciclo siguiente.
"""
# ---------------------------------------------------------------------------
# LIMITACIONES CONOCIDAS
# - El recurso no esta documentado oficialmente: su esquema puede cambiar sin aviso.
#   No se interpreta ningun campo de significado desconocido (codProduct, p y
#   accesible se guardan tal cual).
# - Las posiciones son orientativas: pueden tener retraso e imprecision de GPS.
# - La fuente no ofrece velocidad ni rumbo.
# - No se modela la infraestructura (numero de vias, trazado, estaciones).
#
# ESQUEMA VERIFICADO contra la respuesta real (12-11-2026, 161 trenes): coincide con
# el esperado. Los 14 campos aparecen en todos los trenes; `time` llega como entero y
# `ultRetraso` como texto. No hay diferencias que documentar.
# ---------------------------------------------------------------------------
from __future__ import annotations

import itertools
import json
import logging
import math
import os
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import requests

DEFAULT_URL = "https://tiempo-real.largorecorrido.renfe.com/renfe-visor/flotaLD.json"
MIN_POLL_INTERVAL_SECONDS = 15
HTTP_TIMEOUT_SECONDS = 10
EARTH_RADIUS_M = 6_371_000.0

log = logging.getLogger("renfe_collector")


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"AVISO: {name}={raw!r} no es numerico; se usa {default}")
        return default


ALERT_DISTANCE_METERS = _env_float("ALERT_DISTANCE_METERS", 5000)
POLL_INTERVAL_SECONDS = _env_float("POLL_INTERVAL_SECONDS", 30)
MAX_POSITION_AGE_SECONDS = _env_float("MAX_POSITION_AGE_SECONDS", 300)
RENFE_URL = os.getenv("RENFE_URL") or DEFAULT_URL
SAMPLE_FILE = os.getenv("SAMPLE_FILE") or None
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

DB_HOST = os.getenv("DB_HOST") or None
DB_PORT = int(_env_float("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "renfe")
DB_USER = os.getenv("DB_USER", "renfe")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
MADRID = ZoneInfo("Europe/Madrid")


# --------------------------------------------------------------------------- modelos
@dataclass(frozen=True)
class Train:
    cod_comercial: str
    lat: float
    lon: float
    time: int  # epoch (segundos), propio de cada tren
    received_at: datetime  # recepcion por el colector (UTC)
    cod_est_ant: str | None = None  # estacion anterior (A)
    cod_est_sig: str | None = None  # estacion siguiente (B)
    cod_origen: str | None = None
    cod_destino: str | None = None
    ult_retraso: int | None = None  # minutos
    hora_llegada_sig_est: str | None = None  # se guarda, no se usa en reglas
    mat: str = ""
    # significado no documentado: se guardan tal cual
    cod_product: Any = None
    p: Any = None
    accesible: Any = None

    @property
    def mat_set(self) -> frozenset[str]:
        return frozenset(m.strip() for m in self.mat.split(",") if m.strip())


@dataclass(frozen=True)
class Alert:
    train_a: Train
    train_b: Train
    distance_m: float
    threshold_m: float
    captured_at: datetime  # UTC
    riesgo_mismo_tramo: bool


# --------------------------------------------------------------------------- captura
def fetch_fleet() -> dict:
    """Descarga el JSON de la flota (o lo lee de SAMPLE_FILE). Lanza excepcion si falla."""
    if SAMPLE_FILE:
        with open(SAMPLE_FILE, encoding="utf-8") as f:
            return json.load(f)
    resp = requests.get(RENFE_URL, timeout=HTTP_TIMEOUT_SECONDS)
    resp.raise_for_status()
    if not resp.content.strip():
        raise ValueError("respuesta vacia")
    return resp.json()


# --------------------------------------------------------------------------- parser
def _text(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def parse_trains(
    payload: dict,
    now: datetime,
    max_age_s: float | None = MAX_POSITION_AGE_SECONDS,
) -> tuple[list[Train], list[str]]:
    """Devuelve (trenes validos, avisos).

    Los avisos son "etiqueta: detalle". Las etiquetas "descartado_*" indican un tren
    descartado; el resto son avisos sin descarte. `max_age_s=None` desactiva el
    filtro de antiguedad.
    """
    if not payload or not isinstance(payload, dict):
        return [], ["respuesta_vacia: sin contenido utilizable"]
    entries = payload.get("trenes")
    if not isinstance(entries, list) or not entries:
        return [], ["respuesta_vacia: sin lista de trenes"]

    warnings: list[str] = []
    trains: list[Train] = []
    seen: set[str] = set()
    for i, raw in enumerate(entries):
        if not isinstance(raw, dict):
            warnings.append(f"descartado_formato: entrada {i} no es un objeto")
            continue

        cod = _text(raw.get("codComercial"))
        lat, lon = _number(raw.get("latitud")), _number(raw.get("longitud"))
        if cod is None or lat is None or lon is None:
            warnings.append(f"descartado_campos_ausentes: entrada {i} (codComercial={cod})")
            continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            warnings.append(f"descartado_coordenadas: tren {cod} lat={lat} lon={lon}")
            continue
        if cod in seen:
            warnings.append(f"descartado_duplicado: codComercial {cod} repetido")
            continue

        ts = _number(raw.get("time"))
        if ts is None:
            warnings.append(f"descartado_sin_time: tren {cod}")
            continue
        age = now.timestamp() - ts
        if max_age_s is not None and age > max_age_s:
            warnings.append(f"descartado_antiguo: tren {cod} posicion de hace {age:.0f} s")
            continue

        retraso = None
        if raw.get("ultRetraso") is not None:
            try:
                retraso = int(str(raw["ultRetraso"]).strip())
            except ValueError:
                warnings.append(f"retraso_invalido: tren {cod} ultRetraso={raw['ultRetraso']!r}")

        seen.add(cod)
        trains.append(
            Train(
                cod_comercial=cod,
                lat=lat,
                lon=lon,
                time=int(ts),
                received_at=now,
                cod_est_ant=_text(raw.get("codEstAnt")),
                cod_est_sig=_text(raw.get("codEstSig")),
                cod_origen=_text(raw.get("codOrigen")),
                cod_destino=_text(raw.get("codDestino")),
                ult_retraso=retraso,
                hora_llegada_sig_est=_text(raw.get("horaLlegadaSigEst")),
                mat=_text(raw.get("mat")) or "",
                cod_product=raw.get("codProduct"),
                p=raw.get("p"),
                accesible=raw.get("accesible"),
            )
        )
    return trains, warnings


# --------------------------------------------------------------------------- alertas
def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en metros entre dos coordenadas (formula de Haversine)."""
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def _mismo_tramo(a: Train, b: Train) -> bool:
    return bool(
        a.cod_est_ant and a.cod_est_sig and b.cod_est_ant and b.cod_est_sig
        and a.cod_est_ant != a.cod_est_sig
        and b.cod_est_ant != b.cod_est_sig
        and a.cod_est_ant == b.cod_est_ant
        and a.cod_est_sig == b.cod_est_sig
    )


def find_alerts(trains: list[Train], threshold_m: float, captured_at: datetime) -> list[Alert]:
    """Cada par de trenes distintos se compara una sola vez.

    Alerta solo si estan en el mismo tramo A->B y la distancia es < umbral.
    """
    alerts: list[Alert] = []
    for a, b in itertools.combinations(trains, 2):
        if a.cod_comercial == b.cod_comercial:  # nunca un tren consigo mismo
            continue
        if a.mat_set & b.mat_set:  # misma unidad fisica, dos servicios consecutivos
            continue
        if not _mismo_tramo(a, b):  # distinto tramo A->B, sentido contrario o en estacion
            continue
        d = haversine_m(a.lat, a.lon, b.lat, b.lon)
        if d < threshold_m:  # estrictamente menor
            alerts.append(Alert(a, b, d, threshold_m, captured_at, True))
    return sorted(alerts, key=lambda al: al.distance_m)


# --------------------------------------------------------------------------- base de datos
def db_connect():
    """Conecta a PostgreSQL y crea el esquema si no existe (schema.sql es idempotente)."""
    import psycopg2  # import perezoso: los tests y el modo sin BD no lo necesitan

    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, connect_timeout=5)
    with conn.cursor() as cur, open(SCHEMA_FILE, encoding="utf-8") as f:
        cur.execute(f.read())
    conn.commit()
    return conn


def _utc(epoch: int) -> datetime:
    return datetime.fromtimestamp(epoch, tz=timezone.utc)


def _madrid_to_utc(text: str | None) -> datetime | None:
    """horaLlegadaSigEst viene en hora local de Madrid y sin zona: se normaliza a UTC."""
    if not text:
        return None
    try:
        return datetime.fromisoformat(text).replace(tzinfo=MADRID).astimezone(timezone.utc)
    except ValueError:
        return None


def position_row(t: Train) -> tuple:
    extra = json.dumps({"codProduct": t.cod_product, "p": t.p, "accesible": t.accesible})
    return (t.cod_comercial, t.mat, t.lat, t.lon, _utc(t.time), t.received_at,
            t.cod_est_ant, t.cod_est_sig, t.cod_origen, t.cod_destino, t.ult_retraso,
            _madrid_to_utc(t.hora_llegada_sig_est), extra)


def alert_row(al: Alert) -> tuple:
    a, b = sorted((al.train_a, al.train_b), key=lambda t: t.cod_comercial)  # orden canonico

    def side(t: Train) -> tuple:
        return (t.cod_comercial, t.mat, t.lat, t.lon, t.cod_est_ant, t.cod_est_sig, _utc(t.time))

    return (al.captured_at, al.distance_m, al.threshold_m, al.riesgo_mismo_tramo, *side(a), *side(b))


POSITIONS_SQL = """
    INSERT INTO positions (cod_comercial, mat, lat, lon, position_time, received_at,
        cod_est_ant, cod_est_sig, cod_origen, cod_destino, ult_retraso,
        hora_llegada_sig_est, extra)
    VALUES %s ON CONFLICT (cod_comercial, position_time) DO NOTHING RETURNING 1"""

ALERTS_SQL = """
    INSERT INTO alerts (captured_at, distance_m, threshold_m, riesgo_mismo_tramo,
        train_a_cod, train_a_mat, train_a_lat, train_a_lon, train_a_est_ant, train_a_est_sig,
        train_a_position_time,
        train_b_cod, train_b_mat, train_b_lat, train_b_lon, train_b_est_ant, train_b_est_sig,
        train_b_position_time)
    VALUES %s ON CONFLICT ON CONSTRAINT alerts_par_posiciones_uq DO NOTHING RETURNING 1"""


def save_cycle(conn, trains: list[Train], alerts: list[Alert]) -> tuple[int, int]:
    """Guarda posiciones y alertas en una transaccion. Devuelve (posiciones, alertas) nuevas."""
    from psycopg2.extras import execute_values

    with conn.cursor() as cur:
        new_pos = execute_values(cur, POSITIONS_SQL, [position_row(t) for t in trains], fetch=True)
        new_alerts = (execute_values(cur, ALERTS_SQL, [alert_row(al) for al in alerts], fetch=True)
                      if alerts else [])
    conn.commit()
    return len(new_pos), len(new_alerts)


def persist(conn, trains: list[Train], alerts: list[Alert]):
    """Guarda el ciclo en la BD si esta configurada. Devuelve la conexion (None si fallo)."""
    if not DB_HOST or not trains:
        return conn
    try:  # frontera con la BD: cualquier fallo se registra y se reintenta en el siguiente ciclo
        if conn is None:
            conn = db_connect()
            log.info("Conectado a la base de datos")
        n_pos, n_alerts = save_cycle(conn, trains, alerts)
        log.info("BD: %d posiciones nuevas (de %d), %d alertas nuevas (de %d)",
                 n_pos, len(trains), n_alerts, len(alerts))
    except Exception as exc:
        log.warning("Fallo de base de datos: %s", exc)
        try:
            conn.close()
        except Exception:
            pass
        conn = None
    return conn


# --------------------------------------------------------------------------- salida
def print_cycle(
    now: datetime, trains: list[Train], warnings: list[str], alerts: list[Alert]
) -> None:
    discards = Counter(w.split(":", 1)[0] for w in warnings if w.startswith("descartado_"))
    motivos = ", ".join(f"{n} {k[len('descartado_'):]}" for k, n in discards.items()) or "ninguno"
    print(f"\n=== Lectura {now:%Y-%m-%d %H:%M:%S} UTC | trenes validos: {len(trains)} "
          f"| descartados: {sum(discards.values())} ({motivos}) ===")
    print(f"{'TREN':<8}{'LATITUD':>11}{'LONGITUD':>12}  {'A':<7}{'B':<7}")
    for t in trains:
        print(f"{t.cod_comercial:<8}{t.lat:>11.5f}{t.lon:>12.5f}  "
              f"{t.cod_est_ant or '-':<7}{t.cod_est_sig or '-':<7}")

    if not alerts:
        print(f"\nSin alertas (ningun par de trenes a menos de {ALERT_DISTANCE_METERS:.0f} m).")
        return
    bar = "!" * 72
    print(f"\n{bar}\n  {len(alerts)} ALERTA(S) DE PROXIMIDAD - orientativas, NO es seguridad ferroviaria\n{bar}")
    for al in alerts:
        print(f"[ALERTA] distancia={al.distance_m:.1f} m | umbral={al.threshold_m:.0f} m | "
              f"captura={al.captured_at:%Y-%m-%d %H:%M:%S} UTC | "
              f"riesgo_mismo_tramo={al.riesgo_mismo_tramo}")
        for t in (al.train_a, al.train_b):
            print(f"    tren {t.cod_comercial} mat={t.mat or '-'} "
                  f"({t.lat:.5f}, {t.lon:.5f}) A={t.cod_est_ant or '-'} B={t.cod_est_sig or '-'}")


# --------------------------------------------------------------------------- main
def main() -> None:
    logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
    interval = POLL_INTERVAL_SECONDS
    if interval < MIN_POLL_INTERVAL_SECONDS:
        log.warning("POLL_INTERVAL_SECONDS=%s es menor que el minimo; se usa %s",
                    interval, MIN_POLL_INTERVAL_SECONDS)
        interval = MIN_POLL_INTERVAL_SECONDS
    if SAMPLE_FILE:
        log.info("Modo sin conexion: leyendo %s (sin filtro de antiguedad)", SAMPLE_FILE)
    log.info("Umbral: %.0f m | intervalo: %.0f s", ALERT_DISTANCE_METERS, interval)
    log.info("Base de datos: %s", f"{DB_HOST}:{DB_PORT}/{DB_NAME}" if DB_HOST else "desactivada")

    conn = None
    try:
        while True:
            now = datetime.now(timezone.utc)
            try:
                payload = fetch_fleet()
                trains, warnings = parse_trains(
                    payload, now, None if SAMPLE_FILE else MAX_POSITION_AGE_SECONDS
                )
                for w in warnings:
                    log.warning(w)
                alerts = find_alerts(trains, ALERT_DISTANCE_METERS, now)
                print_cycle(now, trains, warnings, alerts)
                conn = persist(conn, trains, alerts)
            except (requests.RequestException, ValueError, OSError) as exc:
                # HTTP, timeout, JSON invalido o fichero ilegible: se reintenta en el siguiente ciclo
                log.warning("Fallo al obtener/procesar la lectura: %s", exc)
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("Detenido por el usuario (Ctrl+C).")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
