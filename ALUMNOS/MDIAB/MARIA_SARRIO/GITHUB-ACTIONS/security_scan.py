import re
from pathlib import Path

def scan_repository():
    print("Iniciando escaneo de seguridad...")

    # Patrones que pueden indicar claves API expuestas
    pattern = re.compile(
        r"""(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['"][^'"]{12,}['"]"""
    )

    extensions = {
        ".py", ".json", ".yaml", ".yml",
        ".env", ".txt", ".js", ".ts", ".sh"
    }

    findings = []

    for file in Path(".").rglob("*"):
        if not file.is_file():
            continue

        if ".git" in file.parts or "__pycache__" in file.parts:
            continue

        if file.name == "security_scan.py":
            continue

        if file.suffix.lower() not in extensions:
            continue

        try:
            content = file.read_text(encoding="utf-8")
            for line_number, line in enumerate(content.splitlines(), 1):
                if pattern.search(line):
                    findings.append(f"{file}:{line_number}")
        except (UnicodeDecodeError, PermissionError):
            continue

    if findings:
        print("ALERTA: Posibles claves API expuestas:")
        for finding in findings:
            print(finding)
        raise SystemExit(1)

    print("Escaneo completado. No se encontraron claves API expuestas.")

if __name__ == "__main__":
    scan_repository()