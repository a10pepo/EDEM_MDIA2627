
import requests
import math
import os
import time
from datetime import datetime, timezone

URL = "https://gtfsrt.renfe.com/vehicle_positions_LD.json"
UMBRAL = float(os.getenv("ALERT_DISTANCE_METERS", "1000"))
INTERVALO = int(os.getenv("POLL_SECONDS", "15"))


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

    print(f"[{hora_captura:%H:%M:%S}] Trenes: {len(lista)} | Descartados: {descartados} | Alertas: {len(alertas)}")
    for alerta in alertas:
        print("  ALERTA:", alerta)

    time.sleep(INTERVALO)