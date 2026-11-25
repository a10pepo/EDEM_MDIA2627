import os
import math
from datetime import datetime
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="RENFE Proximidad API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "renfe")
DB_USER = os.getenv("DB_USER", "renfe_user")
DB_PASS = os.getenv("DB_PASS", "renfe_pass")


# Modelos Pydantic
class AlertaOut(BaseModel):
    id: int
    vehicle_1_id: str
    vehicle_2_id: str
    distance_meters: float
    threshold_meters: float
    captured_at: datetime


class TrenOut(BaseModel):
    vehicle_id: str
    trip_id: Optional[str]
    route_id: Optional[str]
    latitude: float
    longitude: float
    received_at: datetime


class DistanciaOut(BaseModel):
    tren_1: str
    tren_2: str
    distancia_metros: float
    timestamp_tren_1: datetime
    timestamp_tren_2: datetime


def get_conn():
    try:
        return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error conectando a la base de datos: {e}")


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@app.get("/getAlertas", response_model=list[AlertaOut])
def get_alertas(limit: int = Query(50, ge=1, le=500)):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, vehicle_1_id, vehicle_2_id, distance_meters,
                       COALESCE(threshold_meters, 500) AS threshold_meters, captured_at
                FROM proximity_alerts
                ORDER BY captured_at DESC
                LIMIT %s;
            """, (limit,))
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/getTrenes", response_model=list[TrenOut])
def get_trenes():
    """Endpoint auxiliar para que el frontend pinte todos los trenes recientes."""
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT DISTINCT ON (vehicle_id)
                    vehicle_id, trip_id, route_id, latitude, longitude, received_at
                FROM train_positions
                ORDER BY vehicle_id, received_at DESC;
            """)
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/getTren/{id}", response_model=TrenOut)
def get_tren(id: str):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT vehicle_id, trip_id, route_id, latitude, longitude, received_at
                FROM train_positions
                WHERE vehicle_id = %s
                ORDER BY received_at DESC
                LIMIT 1;
            """, (id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Tren '{id}' no encontrado")
            return row
    finally:
        conn.close()


@app.get("/getDistancia/{trenId1}/{trenId2}", response_model=DistanciaOut)
def get_distancia(trenId1: str, trenId2: str):
    t1 = get_tren(trenId1)
    t2 = get_tren(trenId2)
    dist = round(haversine(t1["latitude"], t1["longitude"], t2["latitude"], t2["longitude"]), 2)
    return {
        "tren_1": trenId1,
        "tren_2": trenId2,
        "distancia_metros": dist,
        "timestamp_tren_1": t1["received_at"],
        "timestamp_tren_2": t2["received_at"],
    }