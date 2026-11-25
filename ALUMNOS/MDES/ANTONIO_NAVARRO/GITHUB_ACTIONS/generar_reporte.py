import json
import sys
from decimal import Decimal
from pathlib import Path


def generar_reporte(ruta_ventas, entorno):
    datos = json.loads(Path(ruta_ventas).read_text(encoding="utf-8"))
    ventas = datos["ventas"]

    total = sum(
        Decimal(str(venta["cantidad"])) * Decimal(str(venta["precio_unitario"]))
        for venta in ventas
    )

    ruta_reporte = Path(f"reporte_{entorno}.txt")
    contenido = (
        f"Entorno: {entorno}\n"
        f"Número de ventas: {len(ventas)}\n"
        f"Total: {total:.2f} €\n"
    )
    ruta_reporte.write_text(contenido, encoding="utf-8")
    print(f"Reporte generado: {ruta_reporte}")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python generar_reporte.py ventas.json entorno")

    entorno = sys.argv[2]
    if entorno not in ("staging", "production"):
        raise SystemExit("El entorno debe ser staging o production")

    generar_reporte(sys.argv[1], entorno)


if __name__ == "__main__":
    main()
