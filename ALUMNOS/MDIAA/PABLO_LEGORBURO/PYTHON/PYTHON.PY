# EJERCICIO 1
texto = "Marina de Empresas 2025"

print(len(texto))
print(texto[0])


# EJERCICIO 2
festivo: bool = True
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")


# EJERCICIO 4
def ultimoCaracter(texto):
    if isinstance(texto, str):
        if len(texto) > 0:
            return texto[-1]
        return ""
    else:
        return 'Debo ser ejecutada con un string'


# EJERCICIO 5 — Bad Words
def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w and not w.startswith("#"):
            bad.add(norm(w))

entrada = input()

if not entrada or " " in entrada:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_normalizada = norm(entrada)
    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
    