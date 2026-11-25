"""
Script de escaneo de seguridad.
Simula la búsqueda de claves API expuestas en archivos del repositorio.
"""

import re
import sys
import os

# Patrones de claves API y secretos que se buscan
API_KEY_PATTERNS = [
    (r'(?i)(api[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', "API Key genérica"),
    (r'(?i)(secret[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', "Secret Key"),
    (r'(?i)(access[_-]?token)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', "Access Token"),
    (r'(?i)(password|passwd)\s*[:=]\s*["\']?([^\s"\']{8,})["\']?', "Contraseña expuesta"),
    (r'sk-[A-Za-z0-9]{32,}', "OpenAI API Key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
]

FILES_TO_SCAN = [
    "data/ventas.json",
    "scripts/security_scan.py",
    ".github/workflows/ejercicio_entregable.yaml",
]


def scan_file(filepath: str) -> list:
    """Escanea un archivo en busca de secretos o claves API expuestas."""
    print(f"  🔍 Escaneando: {filepath}")
    vulnerabilities = []

    if not os.path.exists(filepath):
        print(f"  ⚠️  Archivo no encontrado, se omite: {filepath}")
        return vulnerabilities

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, start=1):
        for pattern, label in API_KEY_PATTERNS:
            if re.search(pattern, line):
                vulnerabilities.append(
                    {
                        "archivo": filepath,
                        "linea": line_num,
                        "tipo": label,
                        "contenido": line.strip()[:80],
                    }
                )

    return vulnerabilities


def main():
    print("=" * 60)
    print("🛡️   ESCÁNER DE SEGURIDAD — Búsqueda de Secretos Expuestos")
    print("=" * 60)
    print()

    all_vulnerabilities = []

    for filepath in FILES_TO_SCAN:
        vulns = scan_file(filepath)
        all_vulnerabilities.extend(vulns)

    print()
    print("📊 RESULTADO DEL ESCANEO")
    print("-" * 60)

    if all_vulnerabilities:
        print(f"❌ Se encontraron {len(all_vulnerabilities)} posible(s) vulnerabilidad(es):\n")
        for vuln in all_vulnerabilities:
            print(f"  Archivo : {vuln['archivo']}")
            print(f"  Línea   : {vuln['linea']}")
            print(f"  Tipo    : {vuln['tipo']}")
            print(f"  Extracto: {vuln['contenido']}")
            print()
        print("🚨 Pipeline detenido por razones de seguridad.")
        sys.exit(1)
    else:
        print("✅ No se encontraron claves API ni secretos expuestos.")
        print("✅ Todos los archivos escaneados están limpios.")

    print("=" * 60)


if __name__ == "__main__":
    main()
