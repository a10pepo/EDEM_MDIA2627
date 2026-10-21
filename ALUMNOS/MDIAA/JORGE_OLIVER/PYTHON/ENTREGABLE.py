# # Ejercicios entregables - Python

# ## Ejercicio 1

titulo:str = "Marina de Empresas 2025"

print("Esta variable contiene un numero total de caracteres de:", len(titulo))

print("La primera letra de la variable es:", titulo[0])

# # ## Ejercicio 2

festivo:bool = True

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# ## Ejercicio 4

def ultimoCaracter (palabra:str = input("Introduce la palabra deseada: ")):
        return (f"Este es su último carácter: {palabra [-1]}")
    

print(ultimoCaracter())

def ultimoCaracter (palabra):
    if type(palabra) is str:
        return (f"Este es su último carácter: {palabra [-1]}")
    else:
        return("Debo ser ejecutada con un string")

print(ultimoCaracter("Hola"))

# ## Ejercicio 5 — **Bad Words**

def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = norm(input("Introduzca una palabra: "))

if palabra == "" or " " in palabra:
    print("Introduzca una palabra (sin espacios).")
else:
    if palabra in bad:
        print ("NO CORRECTA")
    else:
        print("CORRECTA")
