import os
import time
import json
import math
from datetime import datetime, timezone
from itertools import combinations
import requests
import psycopg2

# Api de Renfe
URL = "https://gtfsrt.renfe.com/vehicle_positions_LD.json"
UMBRAL_METROS = float(os.getenv("ALERT_DISTANCE_METERS", "50000"))
INTERVALO_SEGUNDOS = int(os.getenv("POLL_INTERVAL_SECONDS", "15"))
DATABASE_URL = os.getenv("DATABASE_URL")
ARCHIVO_RESPALDO = "vehicle_positions_LD.json"


# Funcion de distancia real entre dos puntos sobre la Tierra
def calcular_distancia_metros(lat1, lon1, lat2, lon2):
    radio_tierra = 6371000
    # Hay que pasar los grados a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dif_lat = math.radians(lat2 - lat1)
    dif_lon = math.radians(lon2 - lon1)

    a = math.sin(dif_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dif_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radio_tierra * c


# Descarga de datos y backup
def obtener_datos_renfe():
    try:
        respuesta = requests.get(URL, timeout=10)
        respuesta.raise_for_status()  # Lanza error si la web responde con fallo HTTP (404, 500...)
        datos = respuesta.json()

        # Conserva una copia local
        with open(ARCHIVO_RESPALDO, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2)
        return datos

    except Exception as error:
        print(f"Aviso: No se pudo conectar con Renfe ({error}). Usando respaldo local...")
        if os.path.exists(ARCHIVO_RESPALDO):
            with open(ARCHIVO_RESPALDO, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        return {}


# Lectura de los datos
def leer_y_limpiar_trenes(datos):
    """Extrae los campos pedidos, valida errores y elimina duplicados."""
    lista_trenes = []
    trenes_ya_vistos = set()
    hora_recepcion = datetime.now(timezone.utc)

    # Si la respuesta viene vacía, devolvemos una lista vacía sin romper el programa
    entidades = datos.get("entity", [])
    if not entidades:
        return []

    for item in entidades:
        vehiculo = item.get("vehicle", {})
        posicion = vehiculo.get("position", {})
        viaje = vehiculo.get("trip", {})
        info_vehiculo = vehiculo.get("vehicle", {})

        # 1. Identificador o matrícula del vehículo
        id_tren = info_vehiculo.get("id") or info_vehiculo.get("label") or item.get("id")
        # 2. Latitud y longitud
        lat = posicion.get("latitude")
        lon = posicion.get("longitude")

        # Validar campos ausentes
        if not id_tren or lat is None or lon is None:
            continue

        # Validar registros duplicados en la misma lectura
        id_tren = str(id_tren).strip()
        if id_tren in trenes_ya_vistos:
            continue

        # Validar coordenadas fuera de rango o nulas (0, 0)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180) or (lat == 0 and lon == 0):
            continue

        trenes_ya_vistos.add(id_tren)

        # 5. Fecha/hora de la posición (si viene en el JSON)
        timestamp = vehiculo.get("timestamp")
        if timestamp:
            hora_posicion = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
        else:
            hora_posicion = None

        # Guardamos el tren con los datos que pide el enunciado
        lista_trenes.append({
            "id": id_tren,
            "lat": float(lat),
            "lon": float(lon),
            "ruta": viaje.get("routeId") or viaje.get("route_id"),
            "viaje": viaje.get("tripId") or viaje.get("trip_id"),
            "hora_posicion": hora_posicion,
            "hora_recepcion": hora_recepcion,
            "raw_payload": json.dumps(item)
        })

    return lista_trenes


# Database
def guardar_en_bd(trenes):
    alertas_guardadas = 0
    # Conectamos con PostgreSQL usando la variable DATABASE_URL
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # 1. Guardar posiciones de cada tren
            for t in trenes:
                cur.execute("""
                    INSERT INTO train_positions
                    (vehicle_id, trip_id, route_id, latitude, longitude, position_timestamp, received_at, raw_payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (t["id"], t["viaje"], t["ruta"], t["lat"], t["lon"],
                      t["hora_posicion"], t["hora_recepcion"], t["raw_payload"]))

            # 2. Calcular distancias y guardar alertas
            for t1, t2 in combinations(trenes, 2):
                dist = calcular_distancia_metros(t1["lat"], t1["lon"], t2["lat"], t2["lon"])
                if dist < UMBRAL_METROS:
                    alertas_guardadas += 1
                    print(f"ALERTA GUARDADA: {t1['id']} <-> {t2['id']} a {dist:.1f} m")
                    cur.execute("""
                        INSERT INTO proximity_alerts
                        (train_1_id, train_2_id, train_1_lat, train_1_lon, train_2_lat, train_2_lon, distance_meters, threshold_meters, detected_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (t1["id"], t2["id"], t1["lat"], t1["lon"], t2["lat"], t2["lon"],
                          round(dist, 2), UMBRAL_METROS, t1["hora_recepcion"]))
        conn.commit()
    return alertas_guardadas


# Bucle listar todo
print(f"Iniciando colector SQL RENFE | Umbral: {UMBRAL_METROS} m | Intervalo: {INTERVALO_SEGUNDOS} s")

while True:
    try:
        datos_json = obtener_datos_renfe()
        trenes = leer_y_limpiar_trenes(datos_json)
        if trenes:
            alertas = guardar_en_bd(trenes)
            print(f"Ciclo OK -> {len(trenes)} trenes guardados en SQL | {alertas} alertas registradas.")
    except Exception as e:
        print(f"Error en ciclo: {e}")

    time.sleep(INTERVALO_SEGUNDOS)