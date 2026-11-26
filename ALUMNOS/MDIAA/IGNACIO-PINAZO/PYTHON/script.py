# Ejercicio 1

frase = "Marina de Empresas 2025"

print(len(frase))
print(frase[0])

# Ejercicio 2

esFestivo = True

if esFestivo:
    print("Hoy es fiesta voy a echarme una siesta")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# Ejercicio 4

def ultimoCaracter(str: str) -> str:
    try:
        return frase[-1]
    except:
        return "Debo ser ejecutada con un string"

# Ejercicio 5

def norm(s: str) -> str:
    return s.lower().strip()

from pathlib import Path

bad = set()
with open(Path(__file__).parent / "bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

entrada = input("Introduce una palabra: ")

if not entrada.strip() or " " in entrada.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(entrada) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

