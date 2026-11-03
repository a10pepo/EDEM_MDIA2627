import json
import re
import sys
from pathlib import Path


API_KEY_PATTERN = re.compile(
    r"""(?i)(?:api[_-]?key|access[_-]?token|secret[_-]?key)\s*["']?\s*[:=]\s*["']?[A-Za-z0-9_./+=-]{8,}"""
)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Uso: {Path(sys.argv[0]).name} <archivo.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"No se pudo leer JSON válido de {path}: {error}", file=sys.stderr)
        return 2

    matches = API_KEY_PATTERN.findall(json.dumps(data))
    if matches:
        print(f"Se detectaron posibles claves API expuestas en {path}.")
        return 1

    print(f"Escaneo de seguridad completado: no se detectaron claves API en {path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
