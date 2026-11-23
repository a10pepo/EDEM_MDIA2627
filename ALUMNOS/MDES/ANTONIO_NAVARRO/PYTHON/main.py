# Ejercicios entregables - Python

# Ejercicio 1
texto = "Marina de Empresas 2025"
print(len(texto))
print(texto[0])

# Ejercicio 2
festivo = False
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# Ejercicio 4
def ultimoCaracter(valor):
    if not isinstance(valor, str):
        return "Debo ser ejecutada con un string"
    if valor == "":
        return ""
    return valor[-1]

print(ultimoCaracter("Python"))
print(ultimoCaracter(123))

# Ejercicio 5 - Bad Words
def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una palabra: ")
if not palabra or any(caracter.isspace() for caracter in palabra):
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")