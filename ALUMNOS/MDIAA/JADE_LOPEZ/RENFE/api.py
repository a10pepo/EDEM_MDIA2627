import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="API Monitorización Trenes RENFE")

# Habilitar CORS para que el frontend pueda hacer peticiones sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@app.get("/health")
def health():
    """Comprueba que la API está operativa."""
    return {"status": "ok"}


@app.get("/trains/latest")
def get_latest_trains():
    """Devuelve la última posición conocida de cada tren activo."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (vehicle_id)
                    vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at
                FROM train_positions
                ORDER BY vehicle_id, received_at DESC;
            """)
            return cur.fetchall()


@app.get("/trains/{vehicle_id}/history")
def get_train_history(vehicle_id: str, limit: int = Query(default=20, le=100)):
    """Devuelve las últimas posiciones registradas de un tren concreto."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at
                FROM train_positions
                WHERE vehicle_id = %s
                ORDER BY received_at DESC
                LIMIT %s;
            """, (vehicle_id, limit))
            rows = cur.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="Vehículo no encontrado")
            return rows


@app.get("/alerts")
def get_alerts(
    max_distance: float = Query(default=None, description="Filtrar por distancia máxima en metros"),
    limit: int = Query(default=50, le=200)
):
    """Devuelve las alertas de proximidad más recientes."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            if max_distance is not None:
                cur.execute("""
                    SELECT * FROM proximity_alerts
                    WHERE distance_meters <= %s
                    ORDER BY detected_at DESC
                    LIMIT %s;
                """, (max_distance, limit))
            else:
                cur.execute("""
                    SELECT * FROM proximity_alerts
                    ORDER BY detected_at DESC
                    LIMIT %s;
                """, (limit,))
            return cur.fetchall()