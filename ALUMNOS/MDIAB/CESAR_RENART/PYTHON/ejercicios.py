#Ejercicio 1
informacion = "Marina de Empresas 2025"

print(len(informacion))

print(informacion[0])

# Ejercicio 2
festivo: bool = True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#Ejercicio 4
def ultimoCaracter(texto):
    if type(texto) != str:
        return "Debo ser ejecutada con un string"
    else:
        return texto[-1]

#Ejercicio 5
def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = norm(input("Escriba una palabra "))

if  len(palabra) == 0 or " "  in palabra:
    print("Introduce una sola palabra (sin espacios).")
elif palabra in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")

