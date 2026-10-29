import json, sys

with open("ventas.json", "r") as file:
    productos = json.load(file)

    for k, v in productos.items():
        if k == "api_key":
            print("API expuesta!")
            sys.exit(1)

    print("No se ha encontrado ninguna API expuesta")