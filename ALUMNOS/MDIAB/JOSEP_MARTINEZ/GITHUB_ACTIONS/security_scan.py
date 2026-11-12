import json

print("Iniciando escaneo de seguridad...")
print("Buscando claves API expuestas en ventas.json...")

with open("ventas.json", "r") as f:
    contenido = f.read()

# Simulación de detección de claves API
if "api_key" in contenido.lower() or "secret" in contenido.lower():
    print("Alerta: Se han detectado posibles claves API expuestas.")
else:
    print("Escaneo completado: No se han encontrado claves API expuestas.")

