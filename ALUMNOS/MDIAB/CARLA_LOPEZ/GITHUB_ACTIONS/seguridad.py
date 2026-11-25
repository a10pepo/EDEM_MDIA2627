with open("ventas.json", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

if "api_key" in contenido.lower():
    print("ERROR: Posible clave API expuesta")
    exit(1)
else:
    print("Tests de seguridad superados")