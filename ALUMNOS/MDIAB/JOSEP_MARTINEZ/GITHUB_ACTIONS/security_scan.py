import json


def revisar_campos(campos):
    for nombre, valor in campos:
        nombre_normalizado = nombre.lower().replace("_", "").replace("-", "")
        if nombre_normalizado in {"apikey", "secret", "clientsecret"}:
            if isinstance(valor, str) and valor.strip():
                raise SystemExit("Se ha detectado una posible clave API expuesta en ventas.json.")
    return dict(campos)


print("Buscando claves API expuestas en ventas.json...")
with open("ventas.json", encoding="utf-8") as archivo:
    json.load(archivo, object_pairs_hook=revisar_campos)

print("Escaneo completado. No se han encontrado claves API expuestas.")
