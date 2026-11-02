import json
import sys

with open("ventas.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

claves_encontradas = 0

for venta in datos["ventas"]:
    for clave in venta:
        if "API" in clave.upper() or "KEY" in clave.upper():
            print(f"Posible clave API encontrada: {clave}")
            claves_encontradas += 1

if claves_encontradas > 0:
    print("Escaneo de seguridad fallido")
    sys.exit(1)
else:
    print("Escaneo de seguridad superado")
