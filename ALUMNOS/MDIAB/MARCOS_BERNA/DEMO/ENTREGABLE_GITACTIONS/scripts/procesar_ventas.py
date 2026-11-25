"""
Procesa ventas.json y genera un reporte .txt distinto para cada entorno.
Uso: python scripts/procesar_ventas.py <entorno>
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

IVA = 0.21


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("staging", "production"):
        print("Uso: python scripts/procesar_ventas.py <staging|production>")
        sys.exit(1)

    entorno = sys.argv[1]
    with open("ventas.json", encoding="utf-8") as f:
        datos = json.load(f)

    ventas = datos["ventas"]
    por_producto = defaultdict(float)
    por_region = defaultdict(float)
    for v in ventas:
        importe = v["cantidad"] * v["precio_unitario"]
        por_producto[v["producto"]] += importe
        por_region[v["region"]] += importe

    total = sum(por_producto.values())
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    run_id = os.getenv("GITHUB_RUN_ID", "local")

    lineas = [
        "=" * 50,
        f"  REPORTE DE VENTAS - ENTORNO: {entorno.upper()}",
        "=" * 50,
        f"Empresa:        {datos['empresa']}",
        f"Periodo:        {datos['periodo']}",
        f"Generado:       {fecha}",
        f"Run ID:         {run_id}",
        f"Nº de ventas:   {len(ventas)}",
        "",
        "--- Ventas por producto ---",
    ]
    for producto, importe in sorted(por_producto.items(), key=lambda x: -x[1]):
        lineas.append(f"  {producto:<15} {importe:>10.2f} {datos['moneda']}")

    lineas += ["", "--- Ventas por región ---"]
    for region, importe in sorted(por_region.items(), key=lambda x: -x[1]):
        lineas.append(f"  {region:<15} {importe:>10.2f} {datos['moneda']}")

    lineas += ["", f"TOTAL (sin IVA): {total:.2f} {datos['moneda']}"]

    if entorno == "staging":
        # Staging: datos de prueba con detalle completo para depuración
        lineas += ["", "--- [STAGING] Detalle de cada venta (debug) ---"]
        for v in ventas:
            lineas.append(
                f"  #{v['id']} {v['fecha']} {v['producto']} x{v['cantidad']} "
                f"@ {v['precio_unitario']} ({v['region']})"
            )
        lineas += ["", "⚠️  Reporte de STAGING: no usar para decisiones de negocio."]
    else:
        # Production: resumen oficial con IVA
        lineas += [
            f"IVA ({int(IVA * 100)}%):        {total * IVA:.2f} {datos['moneda']}",
            f"TOTAL (con IVA): {total * (1 + IVA):.2f} {datos['moneda']}",
            "",
            "✅ Reporte OFICIAL de PRODUCTION.",
        ]

    nombre = f"reporte_{entorno}.txt"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print("\n".join(lineas))
    print(f"\n📄 Reporte generado: {nombre}")


if __name__ == "__main__":
    main()
