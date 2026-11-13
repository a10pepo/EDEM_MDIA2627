"""Escaneo simulado de seguridad: busca claves API expuestas en el repositorio.

Uso: python3 scan_seguridad.py [directorio_raiz]
Exit code 0 = sin hallazgos, 1 = hay hallazgos.
"""
import pathlib
import re
import sys

PATRONES = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "API key genérica": re.compile(r"(?i)api[_-]?key['\"]?\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    "Token de Discord": re.compile(r"[MN][A-Za-z\d]{23,25}\.[\w-]{6}\.[\w-]{27,38}"),
}

EXCLUIDOS = {".git", "node_modules", "__pycache__"}
EXTENSIONES_IGNORADAS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".ico"}


def archivos_a_escanear(raiz: pathlib.Path):
    for ruta in raiz.rglob("*"):
        if not ruta.is_file():
            continue
        if any(parte in EXCLUIDOS for parte in ruta.relative_to(raiz).parts):
            continue
        if ruta.suffix.lower() in EXTENSIONES_IGNORADAS:
            continue
        yield ruta


def escanear(raiz: pathlib.Path) -> int:
    hallazgos = 0
    for ruta in archivos_a_escanear(raiz):
        try:
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
        except OSError as error:
            print(f"[AVISO] no se pudo leer {ruta}: {error}")
            continue
        for nombre, patron in PATRONES.items():
            for numero, linea in enumerate(texto.splitlines(), start=1):
                if patron.search(linea):
                    print(f"[ALERTA] {nombre} posiblemente expuesta en {ruta}:{numero}")
                    hallazgos += 1
    return hallazgos


def main() -> int:
    raiz = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not raiz.is_dir():
        print(f"[ERROR] directorio no encontrado: {raiz}")
        return 2
    print(f"Escaneando {raiz} ...")
    hallazgos = escanear(raiz)
    print(f"Escaneo finalizado: {hallazgos} hallazgo(s)")
    return 1 if hallazgos else 0


if __name__ == "__main__":
    sys.exit(main())