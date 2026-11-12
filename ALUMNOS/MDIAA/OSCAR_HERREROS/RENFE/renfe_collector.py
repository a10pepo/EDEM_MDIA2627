"""Colector de posiciones de trenes Renfe: descarga, detecta proximidad y guarda en Postgres."""
import json
import logging
import math
import os
import sys
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import combinations

import psycopg
from psycopg.types.json import Jsonb

URL = os.getenv("RENFE_URL", "https://tiempo-real.largorecorrido.renfe.com/renfe-visor/flotaLD.json")
ALERT_DISTANCE_METERS = float(os.getenv("ALERT_DISTANCE_METERS", "1000"))
POLL_SECONDS = max(15, int(os.getenv("POLL_SECONDS", "15")))  # la fuente se actualiza cada ~15 s
EARTH_RADIUS_M = 6_371_000
DB_RETRIES = 30

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("collector")


@dataclass(frozen=True)
class Tren:
    vehicle_id: str  # matrícula: única por unidad
    trip_id: str | None  # codComercial: puede repetirse entre trenes
    origen: str | None
    destino: str | None
    est_sig: str | None
    lat: float
    lon: float
    position_ts: datetime | None
    raw: dict

    @property
    def route_id(self):
        return f"{self.origen}-{self.destino}"


@dataclass(frozen=True)
class Alerta:
    a: Tren
    b: Tren
    distancia: float
    umbral: float


# ---------------------------------------------------------------- descarga y parser
def descargar_json(url=URL):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def parsear_tren(t):
    """Convierte un registro del feed en Tren, o None si es inválido."""
    try:
        lat, lon = float(t["latitud"]), float(t["longitud"])
    except (KeyError, TypeError, ValueError):
        return None
    vehicle_id = t.get("mat") or t.get("codComercial")
    if not vehicle_id or not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    ts = t.get("time")
    return Tren(
        vehicle_id=str(vehicle_id),
        trip_id=t.get("codComercial"),
        origen=t.get("codOrigen"),
        destino=t.get("codDestino"),
        est_sig=t.get("codEstSig"),
        lat=lat,
        lon=lon,
        position_ts=datetime.fromtimestamp(int(ts), tz=timezone.utc) if ts else None,
        raw=t,
    )


def cargar_datos(datos):
    """Devuelve {vehicle_id: Tren}, sin registros inválidos ni duplicados."""
    trenes = (parsear_tren(t) for t in (datos or {}).get("trenes") or [])
    return {t.vehicle_id: t for t in trenes if t}


# ---------------------------------------------------------------- alertas
def distancia_metros(lat1, lon1, lat2, lon2):
    """Distancia Haversine en metros."""
    f1, f2 = math.radians(lat1), math.radians(lat2)
    df, dl = f2 - f1, math.radians(lon2 - lon1)
    h = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(h))


def son_comparables(a, b):
    """Mismo origen y destino, o misma estación siguiente."""
    mismo_trayecto = None not in (a.origen, a.destino) and (a.origen, a.destino) == (b.origen, b.destino)
    misma_siguiente = a.est_sig is not None and a.est_sig == b.est_sig
    return mismo_trayecto or misma_siguiente


def calcular_alertas(trenes, umbral=ALERT_DISTANCE_METERS):
    """Cada par comparable se evalúa una sola vez; alerta si distancia < umbral (estricto)."""
    alertas = []
    for a, b in combinations(trenes.values(), 2):
        if son_comparables(a, b):
            d = distancia_metros(a.lat, a.lon, b.lat, b.lon)
            if d < umbral:
                alertas.append(Alerta(a, b, d, umbral))
    return alertas


# ---------------------------------------------------------------- base de datos
def conectar():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "renfe"),
        user=os.getenv("DB_USER", "renfe"),
        password=os.environ["DB_PASSWORD"],
        autocommit=True,
    )


def esperar_bd():
    for intento in range(1, DB_RETRIES + 1):
        try:
            return conectar()
        except psycopg.OperationalError as e:
            log.warning("BD no disponible (%d/%d): %s", intento, DB_RETRIES, e)
            time.sleep(2)
    sys.exit("No se pudo conectar a la BD")


def guardar_posiciones(conn, trenes, received_at):
    # ON CONFLICT: no duplica si la fuente repite la misma posición (vehicle_id, position_timestamp)
    sql = """INSERT INTO train_positions
             (vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at, raw_payload)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
             ON CONFLICT (vehicle_id, position_timestamp) DO NOTHING"""
    filas = [(t.vehicle_id, t.trip_id, t.route_id, t.lat, t.lon, t.position_ts, received_at, Jsonb(t.raw))
             for t in trenes.values()]
    conn.cursor().executemany(sql, filas)


def guardar_alertas(conn, alertas, received_at):
    sql = """INSERT INTO proximity_alerts
             (vehicle_id_a, vehicle_id_b, lat_a, lon_a, lat_b, lon_b, distance_m, threshold_m, captured_at)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    filas = [(x.a.vehicle_id, x.b.vehicle_id, x.a.lat, x.a.lon, x.b.lat, x.b.lon,
              x.distancia, x.umbral, received_at) for x in alertas]
    conn.cursor().executemany(sql, filas)


# ---------------------------------------------------------------- main
def ciclo(conn):
    received_at = datetime.now(timezone.utc)
    trenes = cargar_datos(descargar_json())
    if not trenes:
        log.warning("Respuesta vacía o sin trenes válidos")
        return
    alertas = calcular_alertas(trenes)
    guardar_posiciones(conn, trenes, received_at)
    guardar_alertas(conn, alertas, received_at)
    log.info("trenes=%d alertas=%d (umbral=%s m)", len(trenes), len(alertas), ALERT_DISTANCE_METERS)
    for x in alertas[:5]:
        log.info("  ALERTA %s <-> %s: %.0f m", x.a.vehicle_id, x.b.vehicle_id, x.distancia)


def main():
    conn = esperar_bd()
    while True:
        try:
            ciclo(conn)
        except psycopg.OperationalError:
            conn = esperar_bd()
        except Exception as e:  # HTTP, JSON, etc.: seguir en el siguiente ciclo
            log.error("Error en ciclo: %s", e)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
