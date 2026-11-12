import math
import os
from datetime import datetime
from typing import List

import psycopg
from fastapi import FastAPI, HTTPException, Query
from psycopg.rows import dict_row
from pydantic import BaseModel

app = FastAPI(title="Renfe - proximidad entre trenes",
              description="Datos operativos orientativos; no es un sistema de seguridad ferroviaria.")

# Posiciones más antiguas que esto se consideran no recientes
RECENT_SECONDS = int(os.getenv("RECENT_SECONDS", "300"))


def db():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "renfe"),
        user=os.getenv("DB_USER", "renfe"),
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row,
        connect_timeout=5,
    )


def query(sql, params=()):
    try:
        with db() as conn:
            return conn.execute(sql, params).fetchall()
    except psycopg.Error as e:
        raise HTTPException(503, f"Error de base de datos: {e.__class__.__name__}")


class Tren(BaseModel):
    vehicle_id: str
    trip_id: str | None
    route_id: str | None
    latitude: float
    longitude: float
    position_timestamp: datetime | None
    received_at: datetime


class Alerta(BaseModel):
    id: int
    vehicle_id_a: str
    vehicle_id_b: str
    lat_a: float
    lon_a: float
    lat_b: float
    lon_b: float
    distance_m: float
    threshold_m: float
    captured_at: datetime


class Distancia(BaseModel):
    tren1: str
    tren2: str
    distancia_m: float


LATEST = """SELECT DISTINCT ON (vehicle_id) vehicle_id, trip_id, route_id, latitude, longitude,
                   position_timestamp, received_at
            FROM train_positions
            WHERE received_at > NOW() - make_interval(secs => %s)
            ORDER BY vehicle_id, received_at DESC"""


def haversine(lat1, lon1, lat2, lon2):
    f1, f2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((f2 - f1) / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(a))


@app.get("/getTrenes", response_model=List[Tren], summary="Posiciones recientes de todos los trenes")
def get_trenes():
    return query(LATEST, (RECENT_SECONDS,))


@app.get("/getAlertas", response_model=List[Alerta], summary="Alertas, de más recientes a más antiguas")
def get_alertas(limit: int = Query(50, ge=1, le=1000)):
    return query("SELECT * FROM proximity_alerts ORDER BY captured_at DESC, id DESC LIMIT %s", (limit,))


@app.get("/getTren/{id}", response_model=Tren, summary="Última posición de un tren")
def get_tren(id: str):
    rows = query("""SELECT vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at
                    FROM train_positions WHERE vehicle_id = %s ORDER BY received_at DESC LIMIT 1""", (id,))
    if not rows:
        raise HTTPException(404, f"Tren {id} no encontrado")
    return rows[0]


@app.get("/getDistancia/{trenId1}/{trenId2}", response_model=Distancia,
         summary="Distancia actual en metros entre dos trenes")
def get_distancia(trenId1: str, trenId2: str):
    recientes = {r["vehicle_id"]: r for r in query(LATEST, (RECENT_SECONDS,))}
    for t in (trenId1, trenId2):
        if t not in recientes:
            raise HTTPException(404, f"Tren {t} no existe o no tiene posición reciente")
    a, b = recientes[trenId1], recientes[trenId2]
    return Distancia(tren1=trenId1, tren2=trenId2,
                     distancia_m=haversine(a["latitude"], a["longitude"], b["latitude"], b["longitude"]))
