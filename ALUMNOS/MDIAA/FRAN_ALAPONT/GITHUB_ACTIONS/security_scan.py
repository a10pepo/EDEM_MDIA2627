import json

# Abrimos y cargamos el archivo de ventas
with open("ventas.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Convertimos los datos a texto para buscar palabras sospechosas
contenido = json.dumps(datos).lower()

# Palabras que podrían indicar una clave API expuesta
patrones = ["api_key", "api_secret", "secret_key"]

# Buscamos si aparece alguno de los patrones
for patron in patrones:
    if patron in contenido:
        print(f"ALERTA: Posible clave API expuesta: {patron}")
        exit(1)

print("Escaneo completado: no se detectaron claves API expuestas.")