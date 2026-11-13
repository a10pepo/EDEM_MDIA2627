import time
import math
import requests
from datetime import datetime, timezone
import os
import psycopg2


API_URL = "https://gtfsrt.renfe.com/vehicle_positions_LD.json"
UMBRAL_METROS = 5000  # 5 kilómetros de distancia mínima permitida
INTERVALO_SEGUNDOS = 15


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "renfe_db")
DB_USER = os.getenv("DB_USER", "renfe_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "renfe_password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

def guardar_posicion_en_bd(tren):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO train_positions (vehicle_id, route_id, latitude, longitude) VALUES (%s, %s, %s, %s)",
            (tren['id'], tren['ruta'], tren['lat'], tren['lon'])
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[Error BD Posición]: {e}")

def guardar_alerta_en_bd(t1, t2, distancia):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO train_alerts (vehicle_id_1, vehicle_id_2, distance_meters, lat_1, lon_1, lat_2, lon_2) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (t1['id'], t2['id'], distancia, t1['lat'], t1['lon'], t2['lat'], t2['lon'])
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[Error BD Alerta]: {e}")

# Carga las herramientas necesarias y define de donde descarga los datos, la distancia mínima de alerta y cada cuanto
#tiempo comprueba los trenes



def calcular_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia en metros entre dos coordenadas GPS."""
    R = 6371000  # Radio de la Tierra en metros
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

#Convierte las coordenadas GPS (latitud y longitud) en una distancia real en metros sobre la superficie de la Tierra.



def obtener_trenes():
    """Descarga el JSON de Renfe y extrae los trenes válidos."""
    try:
        respuesta = requests.get(API_URL, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except Exception as e:
        print(f"[Error] No se pudo descargar la API: {e}")
        return []

#Se conecta a la página de Renfe para descargar el archivo JSON. Si hay un fallo de red o la web no responde,
#el programa lo captura en el except para que no se rompa.


    
    trenes = {}
    for entity in datos.get("entity", []):
        vehicle = entity.get("vehicle", {})
        pos = vehicle.get("position", {})
        
        # Obtener ID y coordenadas asegurando que existen
        tren_id = vehicle.get("vehicle", {}).get("id") or entity.get("id")
        lat = pos.get("latitude")
        lon = pos.get("longitude")

        if not tren_id or lat is None or lon is None:
            continue  # Si falta algún dato clave, ignoramos este registro

        # Guardamos el tren (si se repite, se actualiza con la última posición)
        trenes[tren_id] = {
            "id": str(tren_id),
            "lat": float(lat),
            "lon": float(lon),
            "ruta": vehicle.get("trip", {}).get("route_id", "Desconocida")
        }

    return list(trenes.values())

#Recorre el archivo descargado, saca el identificador del tren y sus coordenadas.
#Si a un tren le falta información o la posición, lo descarta.
#Además, evita duplicados guardando cada tren por su ID único.



def comprobar_proximidad(trenes):
    """Compara todos los trenes entre sí (sin repetir ni compararse consigo mismo)."""
    total_alertas = 0
    n = len(trenes)

    for i in range(n):
        for j in range(i + 1, n):
            t1 = trenes[i]
            t2 = trenes[j]

            distancia = calcular_haversine(t1["lat"], t1["lon"], t2["lat"], t2["lon"])

            if distancia < UMBRAL_METROS:
                total_alertas += 1
                print(f"\n🚨 ¡ALERTA! Los trenes {t1['id']} y {t2['id']} están a {distancia:.2f} metros.")
                print(f"   Ruta 1: {t1['ruta']} | Ruta 2: {t2['ruta']}\n")

                guardar_alerta_en_bd(t1, t2, distancia)

    return total_alertas

#Compara todos los trenes entre sí de forma inteligente (sin comparar un tren consigo mismo y sin repetir parejas).
#Si la distancia entre dos trenes es menor de 5.000 metros, salta una alerta por pantalla.



def main():
    print("Esperando a que la base de datos esté lista...")
    while True:
        try:
            conn = get_db_connection()
            conn.close()
            print("¡Conexión exitosa con la base de datos!")
            break
        except Exception:
            time.sleep(2)
            
    print("Iniciando colector sencillo de Renfe...")
    
    while True:
        print(f"\n[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Consultando posiciones...")
        trenes = obtener_trenes()
        print(f"Trenes detectados: {len(trenes)}")

        for tren in trenes:
            guardar_posicion_en_bd(tren)
        
        if len(trenes) > 1:
            alertas = comprobar_proximidad(trenes)
            print(f"Alertas generadas en este ciclo: {alertas}")
        
        print(f"Esperando {INTERVALO_SEGUNDOS} segundos...")
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()

#Es un bucle infinito que controla los tiempos. En cada vuelta: consulta los trenes, los analiza,
#muestra si hay alertas y espera 15 segundos exactos antes de repetir el proceso.