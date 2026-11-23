import os
import time
import json
import math
from datetime import datetime
import requests

# Configuración (lee la variable de entorno o usa 50000 metros por defecto para probar alertas)
URL = "https://gtfsrt.renfe.com/vehicle_positions_LD.json"
UMBRAL_METROS = float(os.getenv("ALERT_DISTANCE_METERS", "50000"))
ARCHIVO_RESPALDO = "vehicle_positions_LD.json"


def calcular_distancia_metros(lat1, lon1, lat2, lon2):
    radio_tierra = 6371000
    #Hay que pasar los grados a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dif_lat = math.radians(lat2 - lat1)
    dif_lon = math.radians(lon2 - lon1)

    a = math.sin(dif_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dif_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radio_tierra * c

print(calcular_distancia_metros(39.4667, -0.3774, 40.4065, -3.6894))