
import sys

print("Iniciando escaneo de seguridad...")

with open("ventas.json", "r", encoding="utf-8") as archivo:
    contenido = archivo.read().lower()

claves_prohibidas = [
    "api_key",
    "apikey",
    "api-key",
    "secret_key",
    "access_token",
    "password"
]

for clave in claves_prohibidas:
    if clave in contenido:
        print("ERROR: Posible clave expuesta detectada:", clave)
        sys.exit(1)

print("Escaneo de seguridad superado correctamente.")
sys.exit(0)
