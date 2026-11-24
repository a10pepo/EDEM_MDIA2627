
print("Iniciando escaneo de seguridad...")

with open("ventas.json", "r") as archivo:
    datos = archivo.read()

if "API_KEY" in datos or "SECRET" in datos:
    print("¡ALERTA! Se ha encontrado una posible clave expuesta.")
    exit(1)
else:
    print("Escaneo completado. No se encontraron claves expuestas.")
