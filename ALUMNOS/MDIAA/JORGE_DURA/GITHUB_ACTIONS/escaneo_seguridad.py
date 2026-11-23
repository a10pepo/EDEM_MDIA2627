"""Escaneo de seguridad simulado: busca claves API expuestas en los ficheros del repositorio.

Si encuentra alguna, termina con código de salida 1 para que GitHub Actions
marque el job como fallido y el pipeline se detenga.
"""
import re
import sys
from pathlib import Path

# Patrones típicos de claves expuestas: nombre legible → expresión regular
PATRONES = {
    "Clave de AWS": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Token de GitHub": re.compile(r"ghp_[A-Za-z0-9]{36}"),
    "API key de Google": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    "Asignación de clave API": re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
}

CARPETAS_IGNORADAS = {".git"}
ESTE_SCRIPT = Path(__file__).name  # no se escanea a sí mismo (contiene los patrones)


def ficheros_a_revisar(raiz):
    for ruta in raiz.rglob("*"):
        if ruta.is_file() and not CARPETAS_IGNORADAS.intersection(ruta.parts) and ruta.name != ESTE_SCRIPT:
            yield ruta


def main():
    revisados = 0
    hallazgos = []
    for ruta in ficheros_a_revisar(Path(".")):
        try:
            texto = ruta.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # ficheros binarios (imágenes, etc.): no se revisan
        revisados += 1
        for num_linea, linea in enumerate(texto.splitlines(), start=1):
            for nombre, patron in PATRONES.items():
                if patron.search(linea):
                    hallazgos.append(f"{ruta}:{num_linea} → {nombre}")

    print(f"🔍 Escaneo de seguridad: {revisados} ficheros revisados")
    if hallazgos:
        print(f"❌ Posibles claves API expuestas: {len(hallazgos)}")
        for h in hallazgos:
            print(f"   - {h}")
        return 1
    print("✅ No se han encontrado claves API expuestas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
