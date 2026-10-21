#Ejercicio 1

texto = "Marina de Empresas 2025"

print(len(texto))
print(texto[0])

#Ejercicio 2

festivo = True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

#Ejercicio 4

def ultimoCaracter(s):
    if not isinstance(s, str):
        return 'Debo ser ejecutada con un string'
    return s[-1]

#Ejercicio 5

def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w and not w.startswith("#"):
            bad.add(norm(w))

palabra = input()

if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
