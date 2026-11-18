"""Backend FastAPI del proyecto RENFE: consulta PostgreSQL y expone posiciones y alertas.

AVISO: ejercicio universitario. Las posiciones son datos orientativos y las alertas NO
constituyen un sistema de seguridad ferroviaria.

Configuracion (variables de entorno):
    DB_HOST (obligatoria), DB_PORT (5432), DB_NAME (renfe), DB_USER (renfe), DB_PASSWORD
    MAX_POSITION_AGE_SECONDS  antiguedad maxima para considerar "reciente" una posicion (300)
Swagger: /docs
"""
from __future__ import annotations

import logging
import math
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Annotated, Any, Iterator

import psycopg2
import psycopg2.extras
from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

log = logging.getLogger("renfe_api")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(),
                    format="%(asctime)s %(levelname)s %(message)s")

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "renfe")
DB_USER = os.getenv("DB_USER", "renfe")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
MAX_POSITION_AGE_SECONDS = float(os.getenv("MAX_POSITION_AGE_SECONDS", "300"))
EARTH_RADIUS_M = 6_371_000.0

TrenId = Annotated[str, Path(min_length=1, max_length=20, pattern=r"^[A-Za-z0-9_-]+$",
                             description="codComercial del tren (texto, conserva ceros a la izquierda)",
                             examples=["03160"])]

app = FastAPI(
    title="API RENFE - posiciones y alertas de proximidad",
    description="Datos orientativos de un ejercicio universitario. "
                "Las alertas NO constituyen un sistema de seguridad ferroviaria.",
    version="1.0.0",
)


# --------------------------------------------------------------------------- modelos
class TrenAlerta(BaseModel):
    cod_comercial: str
    mat: str
    lat: float
    lon: float
    cod_est_ant: str | None
    cod_est_sig: str | None
    position_time: datetime


class AlertaOut(BaseModel):
    id: int
    captured_at: datetime = Field(description="Hora de captura (UTC)")
    distance_m: float = Field(description="Distancia observada en metros")
    threshold_m: float = Field(description="Umbral vigente cuando se generó la alerta, en metros")
    riesgo_mismo_tramo: bool
    tren_a: TrenAlerta
    tren_b: TrenAlerta


class TrenOut(BaseModel):
    cod_comercial: str
    mat: str
    lat: float
    lon: float
    position_time: datetime = Field(description="Hora de la muestra GPS (UTC)")
    received_at: datetime = Field(description="Hora de recepción por el colector (UTC)")
    edad_posicion_s: float = Field(description="Segundos entre la muestra GPS y ahora")
    reciente: bool = Field(description="True si la posición es más joven que MAX_POSITION_AGE_SECONDS")
    cod_est_ant: str | None
    cod_est_sig: str | None
    cod_origen: str | None
    cod_destino: str | None
    ult_retraso: int | None = Field(description="Minutos; el significado de valores negativos no está documentado")
    hora_llegada_sig_est: datetime | None = Field(description="Informativa; a menudo está en el pasado")
    cod_product: Any | None = Field(description="Valor tal cual del feed (sin interpretar)")
    p: Any | None = Field(description="Valor tal cual del feed (sin interpretar)")
    accesible: bool | None = Field(description="Valor tal cual del feed")


class DistanciaOut(BaseModel):
    tren1: TrenOut
    tren2: TrenOut
    distancia_m: float
    calculada_en: datetime


class PosicionOut(BaseModel):
    cod_comercial: str
    mat: str
    lat: float
    lon: float
    position_time: datetime
    edad_posicion_s: float
    cod_est_ant: str | None
    cod_est_sig: str | None
    ult_retraso: int | None


class PosicionesOut(BaseModel):
    generado_en: datetime
    max_antiguedad_s: float = Field(description="Ventana usada para considerar reciente una posición")
    total: int = Field(description="Trenes con posición reciente (sin aplicar `limit`)")
    ultima_recepcion: datetime | None = Field(
        description="Última vez que el colector guardó datos, aunque no sean recientes. "
                    "None si la base de datos está vacía")
    trenes: list[PosicionOut]


class EstelasOut(BaseModel):
    generado_en: datetime
    minutos: int
    estelas: dict[str, list[tuple[float, float, int]]] = Field(
        description="Por tren, lista ordenada de [latitud, longitud, epoch UTC en segundos]")


class ErrorOut(BaseModel):
    detail: str


# --------------------------------------------------------------------------- base de datos
@contextmanager
def get_conn() -> Iterator[Any]:
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, connect_timeout=5)
    try:
        conn.set_session(readonly=True, autocommit=True)  # la API solo lee
        yield conn
    finally:
        conn.close()


def query(sql: str, params: tuple = ()) -> list[dict]:
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@app.exception_handler(psycopg2.OperationalError)
async def db_unavailable(_: Request, exc: psycopg2.OperationalError) -> JSONResponse:
    log.error("Base de datos no disponible: %s", exc)
    return JSONResponse(status_code=503, content={"detail": "Base de datos no disponible"})


@app.exception_handler(psycopg2.Error)
async def db_error(_: Request, exc: psycopg2.Error) -> JSONResponse:
    log.error("Error de base de datos: %s", exc)  # el detalle va al log, no al cliente
    return JSONResponse(status_code=500, content={"detail": "Error interno de base de datos"})


# --------------------------------------------------------------------------- utilidades
def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


LATEST_SQL = """
    SELECT cod_comercial, mat, lat, lon, position_time, received_at, cod_est_ant, cod_est_sig,
           cod_origen, cod_destino, ult_retraso, hora_llegada_sig_est, extra,
           EXTRACT(EPOCH FROM (now() - position_time)) AS edad_s
    FROM positions WHERE cod_comercial = %s
    ORDER BY position_time DESC LIMIT 1"""


def latest_train(cod: str) -> TrenOut | None:
    rows = query(LATEST_SQL, (cod,))
    if not rows:
        return None
    r = rows[0]
    extra = r.pop("extra") or {}
    edad = float(r.pop("edad_s"))
    return TrenOut(**r, edad_posicion_s=round(edad, 1), reciente=edad <= MAX_POSITION_AGE_SECONDS,
                   cod_product=extra.get("codProduct"), p=extra.get("p"),
                   accesible=extra.get("accesible"))


# --------------------------------------------------------------------------- endpoints
@app.get("/getAlertas", response_model=list[AlertaOut], summary="Alertas registradas",
         responses={503: {"model": ErrorOut}})
def get_alertas(limit: int = Query(50, ge=1, le=1000, description="Máximo de alertas a devolver")):
    """Alertas ordenadas de más recientes a más antiguas."""
    rows = query("""
        SELECT id, captured_at, distance_m, threshold_m, riesgo_mismo_tramo,
               train_a_cod, train_a_mat, train_a_lat, train_a_lon, train_a_est_ant,
               train_a_est_sig, train_a_position_time,
               train_b_cod, train_b_mat, train_b_lat, train_b_lon, train_b_est_ant,
               train_b_est_sig, train_b_position_time
        FROM alerts ORDER BY captured_at DESC, id DESC LIMIT %s""", (limit,))

    def side(r: dict, s: str) -> TrenAlerta:
        return TrenAlerta(cod_comercial=r[f"train_{s}_cod"], mat=r[f"train_{s}_mat"],
                          lat=r[f"train_{s}_lat"], lon=r[f"train_{s}_lon"],
                          cod_est_ant=r[f"train_{s}_est_ant"], cod_est_sig=r[f"train_{s}_est_sig"],
                          position_time=r[f"train_{s}_position_time"])

    return [AlertaOut(id=r["id"], captured_at=r["captured_at"], distance_m=r["distance_m"],
                      threshold_m=r["threshold_m"], riesgo_mismo_tramo=r["riesgo_mismo_tramo"],
                      tren_a=side(r, "a"), tren_b=side(r, "b")) for r in rows]


@app.get("/getTren/{id}", response_model=TrenOut, summary="Datos y última posición de un tren",
         responses={404: {"model": ErrorOut}, 503: {"model": ErrorOut}})
def get_tren(id: TrenId):
    tren = latest_train(id)
    if tren is None:
        raise HTTPException(status_code=404, detail=f"Tren {id} no encontrado")
    return tren


@app.get("/getDistancia/{trenId1}/{trenId2}", response_model=DistanciaOut,
         summary="Distancia actual entre dos trenes",
         responses={400: {"model": ErrorOut}, 404: {"model": ErrorOut}, 409: {"model": ErrorOut},
                    503: {"model": ErrorOut}})
def get_distancia(trenId1: TrenId, trenId2: TrenId):
    """Distancia en metros (Haversine) entre las posiciones más recientes de ambos trenes.

    404 si alguno no existe; 409 si la posición de alguno es más antigua que
    `MAX_POSITION_AGE_SECONDS`, porque la distancia no sería representativa.
    """
    if trenId1 == trenId2:
        raise HTTPException(status_code=400, detail="Los dos trenes deben ser distintos")
    trenes = []
    for cod in (trenId1, trenId2):
        t = latest_train(cod)
        if t is None:
            raise HTTPException(status_code=404, detail=f"Tren {cod} no encontrado")
        if not t.reciente:
            raise HTTPException(
                status_code=409,
                detail=f"La posición del tren {cod} no es reciente "
                       f"({t.edad_posicion_s:.0f} s; máximo {MAX_POSITION_AGE_SECONDS:.0f} s)")
        trenes.append(t)
    a, b = trenes
    return DistanciaOut(tren1=a, tren2=b, distancia_m=round(haversine_m(a.lat, a.lon, b.lat, b.lon), 1),
                        calculada_en=datetime.now(timezone.utc))


@app.get("/getPosiciones", response_model=PosicionesOut, summary="Posiciones recientes de los trenes",
         responses={503: {"model": ErrorOut}})
def get_posiciones(limit: int = Query(500, ge=1, le=2000, description="Máximo de trenes a devolver")):
    """Última posición de cada tren con una muestra más joven que `MAX_POSITION_AGE_SECONDS`."""
    rows = query("""
        SELECT * FROM (
            SELECT DISTINCT ON (cod_comercial)
                   cod_comercial, mat, lat, lon, position_time, cod_est_ant, cod_est_sig, ult_retraso,
                   EXTRACT(EPOCH FROM (now() - position_time)) AS edad_s
            FROM positions
            WHERE position_time > now() - make_interval(secs => %s)
            ORDER BY cod_comercial, position_time DESC) recientes
        ORDER BY cod_comercial""", (MAX_POSITION_AGE_SECONDS,))
    last = query("SELECT max(received_at) AS ultima FROM positions")[0]["ultima"]
    trenes = []
    for r in rows:
        edad = round(float(r.pop("edad_s")), 1)
        trenes.append(PosicionOut(**r, edad_posicion_s=edad))
    return PosicionesOut(generado_en=datetime.now(timezone.utc), max_antiguedad_s=MAX_POSITION_AGE_SECONDS,
                         total=len(trenes), ultima_recepcion=last, trenes=trenes[:limit])


@app.get("/getEstelas", response_model=EstelasOut, summary="Estela (posiciones recientes) de cada tren",
         responses={503: {"model": ErrorOut}})
def get_estelas(minutos: int = Query(15, ge=1, le=120, description="Minutos de historial")):
    """Posiciones de los últimos `minutos` de cada tren, para dibujar su recorrido."""
    rows = query("""
        SELECT cod_comercial, lat, lon, EXTRACT(EPOCH FROM position_time)::bigint AS t
        FROM positions
        WHERE position_time > now() - make_interval(mins => %s)
        ORDER BY cod_comercial, position_time""", (minutos,))
    estelas: dict[str, list[tuple[float, float, int]]] = {}
    for r in rows:
        estelas.setdefault(r["cod_comercial"], []).append((r["lat"], r["lon"], r["t"]))
    return EstelasOut(generado_en=datetime.now(timezone.utc), minutos=minutos, estelas=estelas)


@app.get("/health", include_in_schema=False)
def health() -> dict:
    return {"status": "ok"}
