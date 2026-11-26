import json
from pathlib import Path


CAMPOS_SENSIBLES = {"api_key", "apikey", "api_token", "access_token", "secret_key"}


def contiene_clave_api(datos):
    if isinstance(datos, dict):
        for nombre, valor in datos.items():
            campo = nombre.lower().replace("-", "_")
            if campo in CAMPOS_SENSIBLES and isinstance(valor, str) and valor.strip():
                return True
            if contiene_clave_api(valor):
                return True
    elif isinstance(datos, list):
        return any(contiene_clave_api(elemento) for elemento in datos)
    return False


if __name__ == "__main__":
    archivo = Path(__file__).with_name("ventas.json")
    with archivo.open(encoding="utf-8") as contenido:
        datos = json.load(contenido)

    if contiene_clave_api(datos):
        raise SystemExit("Escaneo fallido: posible clave API expuesta en ventas.json.")

    print("Escaneo correcto: no se encontraron claves API en ventas.json.")
