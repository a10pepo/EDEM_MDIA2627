"""
Simulación de un escaneo de seguridad.
Recorre los archivos del repositorio buscando posibles claves API o
secretos expuestos. Si encuentra alguno, termina con código 1 para
que el job de GitHub Actions falle.
"""
import os
import re
import sys

# Patrones típicos de credenciales expuestas
PATRONES = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub Token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "OpenAI / sk- Key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "Discord Webhook": re.compile(r"https://discord(?:app)?\.com/api/webhooks/\d+/[\w-]+"),
    "API key genérica": re.compile(
        r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
        re.IGNORECASE,
    ),
}

IGNORAR_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
EXTENSIONES = {".py", ".json", ".yaml", ".yml", ".txt", ".md", ".env", ".js", ".ts", ".cfg", ".ini"}
ESTE_ARCHIVO = os.path.abspath(__file__)


def escanear(raiz="."):
    hallazgos = []
    archivos = 0
    for carpeta, dirs, ficheros in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        for nombre in ficheros:
            ruta = os.path.join(carpeta, nombre)
            if os.path.abspath(ruta) == ESTE_ARCHIVO:
                continue
            if os.path.splitext(nombre)[1].lower() not in EXTENSIONES and nombre != ".env":
                continue
            archivos += 1
            with open(ruta, encoding="utf-8", errors="ignore") as f:
                for num, linea in enumerate(f, start=1):
                    for tipo, patron in PATRONES.items():
                        if patron.search(linea):
                            hallazgos.append((ruta, num, tipo))
    return archivos, hallazgos


def main():
    print("🔍 Iniciando escaneo de seguridad (búsqueda de claves API expuestas)...")
    archivos, hallazgos = escanear()
    print(f"   Archivos analizados: {archivos}")

    if hallazgos:
        print(f"❌ Se encontraron {len(hallazgos)} posibles secretos expuestos:")
        for ruta, num, tipo in hallazgos:
            print(f"   - {ruta}:{num} -> {tipo}")
        sys.exit(1)

    print("✅ No se encontraron claves API expuestas. Escaneo superado.")


if __name__ == "__main__":
    main()
