import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "renfe")
DB_USER = os.getenv("DB_USER", "renfe_user")
DB_PASS = os.getenv("DB_PASS", "renfe_pass")


def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/data")
def get_data():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Última posición registrada por cada tren
            cur.execute("""
                SELECT DISTINCT ON (vehicle_id)
                    vehicle_id, trip_id, route_id, latitude, longitude, received_at
                FROM train_positions
                ORDER BY vehicle_id, received_at DESC;
            """)
            trains = cur.fetchall()

            # Asegurar que las coordenadas son float para Leaflet
            for t in trains:
                t['latitude'] = float(t['latitude'])
                t['longitude'] = float(t['longitude'])

            # Últimas 20 alertas de proximidad
            cur.execute("""
                SELECT id, vehicle_1_id, vehicle_2_id, lat_1, lon_1, lat_2, lon_2,
                       distance_meters, threshold_meters, captured_at
                FROM proximity_alerts
                ORDER BY captured_at DESC
                LIMIT 20;
            """)
            alerts = cur.fetchall()
        return {"trains": trains, "alerts": alerts}
    finally:
        conn.close()