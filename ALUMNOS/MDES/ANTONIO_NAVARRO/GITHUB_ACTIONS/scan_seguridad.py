import json
import sys
from pathlib import Path


def buscar_claves(datos, ruta=""):
    encontradas = []

    if isinstance(datos, dict):
        for clave, valor in datos.items():
            ruta_actual = f"{ruta}.{clave}" if ruta else clave

            # Comprobamos nombres de campos que podrían guardar credenciales.
            if any(texto in clave.lower() for texto in ("api_key", "apikey", "token", "secret")) and valor:
                encontradas.append(ruta_actual)

            encontradas.extend(buscar_claves(valor, ruta_actual))

    elif isinstance(datos, list):
        for indice, valor in enumerate(datos):
            encontradas.extend(buscar_claves(valor, f"{ruta}[{indice}]"))

    return encontradas


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scan_seguridad.py ventas.json")

    datos = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    encontradas = buscar_claves(datos)

    if encontradas:
        print("Posibles claves expuestas en:", ", ".join(encontradas))
        raise SystemExit(1)

    print("No se han encontrado claves API expuestas.")


if __name__ == "__main__":
    main()
