print("Comprobando seguridad en ventas.json...")

with open("ventas.json", "r", encoding="utf-8") as archivo:
    datos = archivo.read()

if "API_KEY" in datos or "SECRET" in datos:
    print("Error: se detectó una posible clave sensible dentro del archivo.")
    exit(1)
else:
    print("Todo correcto: archivo limpio de claves sensibles.")