import os
import time
import json
import math
import logging
from datetime import datetime, timezone
from itertools import combinations
import requests
import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuración mediante variables de entorno
RENFE_URL = os.getenv("RENFE_URL", "https://gtfsrt.renfe.com/vehicle_positions_LD.json")
ALERT_DISTANCE_METERS = float(os.getenv("ALERT_DISTANCE_METERS", "500"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "renfe")
DB_USER = os.getenv("DB_USER", "renfe_user")
DB_PASS = os.getenv("DB_PASS", "renfe_pass")


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula la distancia en metros entre dos coordenadas GPS."""
    R = 6371000.0  # Radio de la Tierra en metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_db_connection():
    while True:
        try:
            return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        except psycopg2.OperationalError:
            logging.warning("Esperando a que PostgreSQL esté listo...")
            time.sleep(3)


def fetch_and_parse() -> list[dict]:
    """Descarga, valida y normaliza el feed GTFS-RT JSON."""
    try:
        resp = requests.get(RENFE_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logging.error(f"Error consultando API de Renfe: {e}")
        return []

    entities = data.get("entity", [])
    seen_vehicles = set()
    valid_trains = []
    now_utc = datetime.now(timezone.utc)

    for entity in entities:
        vehicle_data = entity.get("vehicle") or {}
        position = vehicle_data.get("position") or {}
        vehicle_desc = vehicle_data.get("vehicle") or {}
        trip = vehicle_data.get("trip") or {}

        v_id = vehicle_desc.get("id") or entity.get("id")
        lat = position.get("latitude")
        lon = position.get("longitude")

        # Validaciones básicas y deduplicación en el mismo ciclo
        if not v_id or lat is None or lon is None:
            continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            continue
        if v_id in seen_vehicles:
            continue
        seen_vehicles.add(v_id)

        ts_raw = vehicle_data.get("timestamp")
        pos_ts = datetime.fromtimestamp(int(ts_raw), tz=timezone.utc) if ts_raw else None

        valid_trains.append({
            "vehicle_id": str(v_id),
            "trip_id": trip.get("tripId"),
            "route_id": trip.get("routeId"),
            "latitude": float(lat),
            "longitude": float(lon),
            "position_timestamp": pos_ts,
            "received_at": now_utc,
            "raw_payload": json.dumps(entity),
        })

    return valid_trains


def process_cycle(conn):
    trains = fetch_and_parse()
    if not trains:
        logging.info("Sin registros válidos en esta lectura.")
        return

    alerts = []
    # Compara cada par único sin repetir ni comparar un tren consigo mismo
    for t1, t2 in combinations(trains, 2):
        dist = haversine(t1["latitude"], t1["longitude"], t2["latitude"], t2["longitude"])
        if dist < ALERT_DISTANCE_METERS:
            alerts.append((
                t1["vehicle_id"], t2["vehicle_id"],
                t1["latitude"], t1["longitude"],
                t2["latitude"], t2["longitude"],
                round(dist, 2),
                ALERT_DISTANCE_METERS,  # <-- Se añade aquí
                t1["received_at"]
            ))
            logging.warning(
                f"ALERTA PROXIMIDAD: {t1['vehicle_id']} y {t2['vehicle_id']} a {dist:.1f} m"
            )

    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO train_positions 
            (vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at, raw_payload)
            VALUES %s
            """,
            [
                (
                    t["vehicle_id"], t["trip_id"], t["route_id"],
                    t["latitude"], t["longitude"], t["position_timestamp"],
                    t["received_at"], t["raw_payload"]
                )
                for t in trains
            ]
        )

        if alerts:
            execute_values(
                cur,
                """
                INSERT INTO proximity_alerts 
                (vehicle_1_id, vehicle_2_id, lat_1, lon_1, lat_2, lon_2, distance_meters, threshold_meters, captured_at)
                VALUES %s
                """,
                alerts
            )
    conn.commit()
    logging.info(f"Guardados {len(trains)} trenes y {len(alerts)} alertas.")


if __name__ == "__main__":
    logging.info(f"Iniciando colector (Umbral: {ALERT_DISTANCE_METERS}m, Intervalo: {POLL_INTERVAL}s)")
    connection = get_db_connection()
    try:
        while True:
            process_cycle(connection)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Deteniendo colector...")
    finally:
        connection.close()