"""Simulación de un escaneo de seguridad en busca de claves API expuestas.

Recorre los ficheros de texto del repositorio y busca patrones típicos de
credenciales (AWS, GitHub, OpenAI/Stripe, Google, Slack, asignaciones del tipo
api_key = "..."). Si encuentra alguna, la muestra enmascarada y termina con
código de salida 1 para que el job falle.

Uso: python security_scan.py [directorio]   (por defecto, el directorio actual)
"""

import os
import re
import sys

PATRONES = {
    "AWS Access Key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub Token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Clave tipo sk- (OpenAI/Stripe)": re.compile(r"\bsk-(?:live_|test_|proj-)?[A-Za-z0-9_-]{20,}\b"),
    "Google API Key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Slack Token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Asignación de clave en claro": re.compile(
        r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|password)\b\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']"
    ),
}

DIRECTORIOS_IGNORADOS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
EXTENSIONES_BINARIAS = {".pdf", ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".pyc"}
FICHEROS_IGNORADOS = {".coverage", os.path.basename(__file__)}


def enmascarar(valor: str) -> str:
    if len(valor) <= 8:
        return "*" * len(valor)
    return f"{valor[:4]}{'*' * (len(valor) - 8)}{valor[-4:]}"


def escanear(raiz: str) -> list:
    hallazgos = []
    for carpeta, subcarpetas, ficheros in os.walk(raiz):
        subcarpetas[:] = [d for d in subcarpetas if d not in DIRECTORIOS_IGNORADOS]
        for nombre in ficheros:
            if nombre in FICHEROS_IGNORADOS or os.path.splitext(nombre)[1].lower() in EXTENSIONES_BINARIAS:
                continue
            ruta = os.path.join(carpeta, nombre)
            try:
                with open(ruta, encoding="utf-8") as f:
                    for num_linea, linea in enumerate(f, start=1):
                        for tipo, patron in PATRONES.items():
                            for m in patron.finditer(linea):
                                hallazgos.append((os.path.relpath(ruta, raiz), num_linea, tipo, enmascarar(m.group(0))))
            except (UnicodeDecodeError, OSError):
                continue
    return hallazgos


def main() -> int:
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"🔍 Escaneando '{os.path.abspath(raiz)}' en busca de claves API expuestas...")
    hallazgos = escanear(raiz)
    if hallazgos:
        print(f"❌ Se han encontrado {len(hallazgos)} posibles secretos expuestos:")
        for ruta, linea, tipo, valor in hallazgos:
            print(f"   - {ruta}:{linea} -> {tipo}: {valor}")
        return 1
    print("✅ Escaneo completado: no se han encontrado claves API expuestas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
