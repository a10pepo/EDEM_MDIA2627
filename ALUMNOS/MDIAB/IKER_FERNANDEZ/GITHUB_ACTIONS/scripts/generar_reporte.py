"""Procesa ventas.json y genera un reporte .txt para el entorno indicado.

Uso: python generar_reporte.py <entorno> <ruta_ventas_json> <directorio_salida>
Genera <directorio_salida>/reporte_<entorno>.txt
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone


def main() -> int:
    if len(sys.argv) != 4:
        print("Uso: python generar_reporte.py <entorno> <ventas.json> <directorio_salida>")
        return 2

    entorno, ruta_json, salida = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(ruta_json, encoding="utf-8") as f:
        datos = json.load(f)

    ventas = datos["ventas"]
    moneda = datos.get("moneda", "EUR")
    total = 0.0
    unidades = 0
    por_categoria = defaultdict(float)
    por_region = defaultdict(float)
    for v in ventas:
        importe = v["unidades"] * v["precio_unitario"]
        total += importe
        unidades += v["unidades"]
        por_categoria[v["categoria"]] += importe
        por_region[v["region"]] += importe

    lineas = [
        "=" * 50,
        f"REPORTE DE VENTAS - ENTORNO: {entorno.upper()}",
        "=" * 50,
        f"Empresa:            {datos.get('empresa', '-')}",
        f"Periodo:            {datos.get('periodo', '-')}",
        f"Generado (UTC):     {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        f"Commit:             {os.environ.get('GITHUB_SHA', 'local')[:7]}",
        f"Ejecución:          #{os.environ.get('GITHUB_RUN_NUMBER', '-')}",
        "",
        f"Nº de operaciones:  {len(ventas)}",
        f"Unidades vendidas:  {unidades}",
        f"Importe total:      {total:,.2f} {moneda}",
        f"Ticket medio:       {total / len(ventas):,.2f} {moneda}",
        "",
        "Ventas por categoría:",
        *[f"  - {c:<15} {imp:>12,.2f} {moneda}" for c, imp in sorted(por_categoria.items(), key=lambda x: -x[1])],
        "",
        "Ventas por región:",
        *[f"  - {r:<15} {imp:>12,.2f} {moneda}" for r, imp in sorted(por_region.items(), key=lambda x: -x[1])],
        "",
    ]
    if entorno == "production":
        lineas.append("Estado: datos PUBLICADOS en el entorno de producción.")
    else:
        lineas.append("Estado: datos VALIDADOS en staging (pendiente de pasar a producción).")

    os.makedirs(salida, exist_ok=True)
    ruta_reporte = os.path.join(salida, f"reporte_{entorno}.txt")
    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print("\n".join(lineas))
    print(f"📄 Reporte guardado en {ruta_reporte}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
