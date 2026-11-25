import json
import sys

print("Iniciando análisis de seguridad en ventas.json...")

#   Intentamos abrir y cargar el archivo de ventas
try:
    with open("ventas.json", "r", encoding="utf-8") as fichero:
        registros = json.load(fichero)
except FileNotFoundError:
    print("ERROR: No se encuentra el archivo ventas.json en el repositorio.")
    sys.exit(1)
    
# Convertimos los datos a texto para buscar palabras sospechosas
texto_ventas = json.dumps(registros).lower()

palabras_prohibidas = ["api_key", "secret_key", "access_token", "private_key"]

for palabra in palabras_prohibidas:
    if palabra in texto_ventas:
        print(f"ERROR DE SEGURIDAD: Se detectó una posible credencial ({palabra})")
        sys.exit(1)

print("Análisis finalizado con éxito: no hay claves API expuestas.")