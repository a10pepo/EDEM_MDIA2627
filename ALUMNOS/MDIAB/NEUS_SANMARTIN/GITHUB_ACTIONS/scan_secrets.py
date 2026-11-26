import re, sys

patrones = [
    r"AKIA[0-9A-Z]{16}",
    r"sk-[A-Za-z0-9]{20,}",
    r"(?i)api[_-]?key\"?\s*[:=]\s*\"?[A-Za-z0-9]{16,}",
]
contenido = open(sys.argv[1]).read()

if any(re.search(p, contenido) for p in patrones):
    print("¡Posibles claves API expuestas!")
    sys.exit(1)
print("Escaneo OK: no se encontraron claves API.")