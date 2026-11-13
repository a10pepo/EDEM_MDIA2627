import os
import math
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Renfe Tracking API", version="1.0")

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "renfe_db")
DB_USER = os.getenv("DB_USER", "renfe_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "renfe_password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

def calcular_haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class AlertaResponse(BaseModel):
    id: int
    vehicle_id_1: str
    vehicle_id_2: str
    distance_meters: float
    lat_1: float
    lon_1: float
    lat_2: float
    lon_2: float

class TrenResponse(BaseModel):
    vehicle_id: str
    route_id: str | None
    latitude: float
    longitude: float
    received_at: str

@app.get("/getAlertas", response_model=list[AlertaResponse])
def get_alertas(limit: int = Query(50, ge=1, le=500)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM train_alerts ORDER BY id DESC LIMIT %s", (limit,))
        alertas = cur.fetchall()
        cur.close()
        conn.close()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")

@app.get("/getTren/{id}", response_model=TrenResponse)
def get_tren(id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT vehicle_id, route_id, latitude, longitude, received_at FROM train_positions WHERE vehicle_id = %s ORDER BY received_at DESC LIMIT 1",
            (id,)
        )
        tren = cur.fetchone()
        cur.close()
        conn.close()

        if not tren:
            raise HTTPException(status_code=404, detail=f"Tren con ID {id} no encontrado")
        
        tren["received_at"] = str(tren["received_at"])
        return tren
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")

@app.get("/getDistancia/{trenId1}/{trenId2}")
def get_distancia(trenId1: str, trenId2: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT latitude, longitude, received_at FROM train_positions WHERE vehicle_id = %s ORDER BY received_at DESC LIMIT 1", (trenId1,))
        t1 = cur.fetchone()

        cur.execute("SELECT latitude, longitude, received_at FROM train_positions WHERE vehicle_id = %s ORDER BY received_at DESC LIMIT 1", (trenId2,))
        t2 = cur.fetchone()

        cur.close()
        conn.close()

        if not t1 or not t2:
            raise HTTPException(status_code=404, detail="Uno de los trenes no existe o no tiene posiciones registradas")

        distancia = calcular_haversine(t1["latitude"], t1["longitude"], t2["latitude"], t2["longitude"])
        
        return {
            "tren_1": trenId1,
            "tren_2": trenId2,
            "distancia_metros": round(distancia, 2)
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")