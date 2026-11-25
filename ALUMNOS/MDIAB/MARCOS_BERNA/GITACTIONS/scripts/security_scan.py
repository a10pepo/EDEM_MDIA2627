"""Simulación de un escaneo de seguridad que busca claves API expuestas.

Recorre los archivos del repositorio y busca patrones típicos de credenciales.
Termina con código 1 si encuentra alguna, para que el job falle.
"""
import os
import re
import sys

PATRONES = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub Token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "OpenAI/Stripe Secret Key": re.compile(r"sk_?(live|test)?[-_][A-Za-z0-9]{20,}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    "Slack Token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "Clave genérica (api_key/secret/token = '...')": re.compile(
        r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"
    ),
}

DIRECTORIOS_IGNORADOS = {".git", "node_modules", "__pycache__", ".venv"}
ESTE_ARCHIVO = os.path.abspath(__file__)


def escanear(raiz: str) -> list[tuple[str, int, str]]:
    hallazgos = []
    for carpeta, subcarpetas, archivos in os.walk(raiz):
        subcarpetas[:] = [d for d in subcarpetas if d not in DIRECTORIOS_IGNORADOS]
        for nombre in archivos:
            ruta = os.path.join(carpeta, nombre)
            if os.path.abspath(ruta) == ESTE_ARCHIVO:
                continue
            try:
                with open(ruta, encoding="utf-8") as f:
                    for n_linea, linea in enumerate(f, start=1):
                        for tipo, patron in PATRONES.items():
                            if patron.search(linea):
                                hallazgos.append((ruta, n_linea, tipo))
            except (UnicodeDecodeError, OSError):
                continue  # archivos binarios o ilegibles
    return hallazgos


def main() -> int:
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"🔍 Escaneando '{raiz}' en busca de claves API expuestas...")
    hallazgos = escanear(raiz)
    if hallazgos:
        print(f"❌ Se encontraron {len(hallazgos)} posibles credenciales expuestas:")
        for ruta, n_linea, tipo in hallazgos:
            print(f"   - {ruta}:{n_linea} -> {tipo}")
        return 1
    print("✅ No se encontraron claves API expuestas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
