"""Genera un reporte de ventas en .txt distinto para cada entorno."""
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone

CONFIG_ENTORNOS = {
    "staging": {"titulo": "REPORTE DE VENTAS - STAGING (pruebas)", "iva": 0.0,
                "nota": "Datos de prueba. No usar para decisiones de negocio."},
    "production": {"titulo": "REPORTE DE VENTAS - PRODUCTION", "iva": 0.21,
                   "nota": "Reporte oficial para el jefe de departamento."},
}


def main() -> int:
    archivo, entorno = sys.argv[1], sys.argv[2]
    if entorno not in CONFIG_ENTORNOS:
        print(f"Entorno desconocido: {entorno}")
        return 1
    cfg = CONFIG_ENTORNOS[entorno]

    with open(archivo, encoding="utf-8") as f:
        datos = json.load(f)

    ventas = datos["ventas"]
    total = sum(v["cantidad"] * v["precio_unitario"] for v in ventas)
    por_region = defaultdict(float)
    for v in ventas:
        por_region[v["region"]] += v["cantidad"] * v["precio_unitario"]

    lineas = [
        "=" * 50,
        cfg["titulo"],
        "=" * 50,
        f"Empresa:  {datos['empresa']}",
        f"Periodo:  {datos['periodo']}",
        f"Entorno:  {entorno}",
        f"Generado: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
        "",
        f"Número de ventas: {len(ventas)}",
        f"Total (sin IVA):  {total:,.2f} {datos['moneda']}",
        f"IVA aplicado:     {cfg['iva'] * 100:.0f}%",
        f"Total final:      {total * (1 + cfg['iva']):,.2f} {datos['moneda']}",
        "",
        "Ventas por región:",
        *[f"  - {r}: {imp:,.2f} {datos['moneda']}" for r, imp in sorted(por_region.items())],
        "",
        f"Nota: {cfg['nota']}",
    ]

    salida = f"reporte_{entorno}.txt"
    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"✅ Reporte generado: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
