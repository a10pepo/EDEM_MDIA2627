#!/usr/bin/env python3
"""Simulacion de escaneo de seguridad: busca claves API expuestas.

Recorre los ficheros de texto del repositorio y busca patrones tipicos de
credenciales. Termina con codigo 1 si encuentra alguno (el step falla).
Uso: python scripts/escaneo_seguridad.py [directorio]
"""
import re
import sys
from pathlib import Path

PATRONES = {
    "Clave generica (api_key/secret/token = ...)": re.compile(
        r"""(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}"""
    ),
    "AWS Access Key ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Discord webhook": re.compile(r"https://discord(?:app)?\.com/api/webhooks/\d+/[\w\-]+"),
}
IGNORAR_DIRS = {".git", "node_modules", "__pycache__"}
IGNORAR_FICHEROS = {"escaneo_seguridad.py"}  # este script contiene los patrones


def escanear(raiz: Path) -> list[tuple[str, int, str]]:
    hallazgos = []
    for ruta in raiz.rglob("*"):
        if not ruta.is_file() or IGNORAR_DIRS & set(ruta.parts):
            continue
        if ruta.name in IGNORAR_FICHEROS:
            continue
        try:
            lineas = ruta.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue  # binarios o ilegibles
        for n, linea in enumerate(lineas, start=1):
            for nombre, patron in PATRONES.items():
                if patron.search(linea):
                    hallazgos.append((f"{ruta}:{n}", nombre, ""))
    return hallazgos


def main() -> int:
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"[SEGURIDAD] Escaneando '{raiz.resolve()}' en busca de claves API expuestas...")
    hallazgos = escanear(raiz)
    if hallazgos:
        print(f"[SEGURIDAD] ERROR: {len(hallazgos)} posible(s) credencial(es) expuesta(s):")
        for ubicacion, tipo, _ in hallazgos:
            print(f"  - {ubicacion}  ({tipo})")  # no se imprime el valor
        return 1
    print("[SEGURIDAD] OK: no se han encontrado claves API expuestas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
