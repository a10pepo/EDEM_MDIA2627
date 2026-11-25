import sys

with open("ventas.json", "r") as archivo:
    contenido = archivo.read().lower()

if "api_key" in contenido or "secret" in contenido or "password" in contenido or "token" in contenido:
    print("ALERTA: Posible clave API expuesta en ventas.json")
    sys.exit(1) # Para que GitHub Actions interprete que el test ha fallado y el pipeline frene en seco

print("Escaneo limpio: No hay credenciales expuestas.")