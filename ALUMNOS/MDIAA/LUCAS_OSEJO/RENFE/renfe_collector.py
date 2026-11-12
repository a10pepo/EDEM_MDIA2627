
import requests
import math
import os
import time
from datetime import datetime, timezone
import json
import psycopg2

URL = "https://gtfsrt.renfe.com/vehicle_positions_LD.json"
UMBRAL = float(os.getenv("ALERT_DISTANCE_METERS", "1000"))
INTERVALO = int(os.getenv("POLL_SECONDS", "15"))

def conectar():
    while True:
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            )
        except psycopg2.OperationalError as e:
            print("Esperando a la base de datos...", e)
            time.sleep(3)

conn = conectar()
conn.autocommit = True
cur = conn.cursor()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))


while True:
    try:
        respuesta = requests.get(URL, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except Exception as e:
        print("Error al leer la API:", e)
        time.sleep(INTERVALO)
        continue

    hora_captura = datetime.now(timezone.utc)
    ts = datos.get("header", {}).get("timestamp")
    hora_posicion = datetime.fromtimestamp(int(ts), timezone.utc) if ts else None
    

    trenes = {}
    descartados = 0
    for entidad in datos.get("entity", []):
        vehiculo = entidad.get("vehicle", {})
        vehicle_id = vehiculo.get("vehicle", {}).get("id")
        lat = vehiculo.get("position", {}).get("latitude")
        lon = vehiculo.get("position", {}).get("longitude")
        trip_id = vehiculo.get("trip", {}).get("tripId")

        if vehicle_id is None or lat is None or lon is None:
            descartados += 1
            continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            descartados += 1
            continue
        if vehicle_id in trenes:
            continue

        trenes[vehicle_id] = {"vehicle_id": vehicle_id, "trip_id": trip_id, "lat": lat, "lon": lon}

    lista = list(trenes.values())
    alertas = []
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            a = lista[i]
            b = lista[j]
            d = haversine(a["lat"], a["lon"], b["lat"], b["lon"])
            if d < UMBRAL:
                alertas.append({
                    "tren_1": a["vehicle_id"], "lat_1": a["lat"], "lon_1": a["lon"],
                    "tren_2": b["vehicle_id"], "lat_2": b["lat"], "lon_2": b["lon"],
                    "distancia_m": round(d, 1),
                    "umbral_m": UMBRAL,
                    "hora_captura": hora_captura.isoformat(),
                })

    for t in lista:
        cur.execute(
            """INSERT INTO train_positions
               (vehicle_id, trip_id, latitude, longitude, position_timestamp, received_at, raw_payload)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (vehicle_id, position_timestamp) DO NOTHING""",
            (t["vehicle_id"], t["trip_id"], t["lat"], t["lon"], hora_posicion, hora_captura, json.dumps(t)),
        )

    for al in alertas:
        cur.execute(
            """INSERT INTO train_alerts
               (vehicle_id_1, vehicle_id_2, latitude_1, longitude_1, latitude_2, longitude_2,
                distance_m, threshold_m, captured_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (al["tren_1"], al["tren_2"], al["lat_1"], al["lon_1"], al["lat_2"], al["lon_2"],
             al["distancia_m"], al["umbral_m"], hora_captura),
        )

    print(f"[{hora_captura:%H:%M:%S}] Trenes: {len(lista)} | Descartados: {descartados} | Alertas: {len(alertas)}")
    for alerta in alertas:
        print("  ALERTA:", alerta)

    time.sleep(INTERVALO)