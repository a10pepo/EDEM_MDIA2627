import json
import sys

def escaneAPI():
    with open ("./ventas.json", "r") as file:

        data = json.load(file)
        cont = 0
        for key in data.keys():
            if "API" in key.upper() or "KEY" in key.upper():
                print(f"Se ha encontrado una clave: {key}")
                cont += 1

        if cont == 0:
            return True
        else:
            return False

if not escaneAPI():
    sys.exit(1)
print("No se han encontrado claves expuestas")
