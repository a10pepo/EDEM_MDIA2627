from pathlib import Path
import sys

archivo_ventas = Path(__file__).with_name("ventas.json")

try:
    contenido = archivo_ventas.read_text(encoding="utf-8").casefold()
except FileNotFoundError:
    print(f"Error: no se encuentra {archivo_ventas.name}")
    sys.exit(1)

indicadores = ("api_key", "apikey", "api-key")
coincidencias = [indicador for indicador in indicadores if indicador in contenido]

if coincidencias:
    print("Aviso: se ha encontrado un posible indicador de clave API en ventas.json")
    sys.exit(1)

print("Revisión completada: no se han encontrado indicadores de claves API")
