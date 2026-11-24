# Ejercicios entregables - Python

## Ejercicio 1
1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025” 
variable= "Marina de empresas"

2. Muestra por consola la longitud de la variable 
long = len(variable) 
print(f"La longitud de la variable {variable} es {long}")

3. Utilizando esa variable muestra por consola la primera letra.
print(f"La primera letrad es {variable[0]}")

## Ejercicio 2
1. Define una variable festivo que sea de tipo booleano. 
festivo = True

2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” 

if festivo==True: 
    print("Hoy es fiesta voy a echarme una siesta!!")
else: 
     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


## Ejercicio 4
1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 
2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 

def ultimocaracter(p):
    if type(p)==str: 
        return f"El último caracter de {p} es {p[-1]}"
    else: 
        return "Debo ser ejecutada con un string"

print(ultimocaracter(124))
print(ultimocaracter("Mamen"))
print(ultimocaracter("La casa de la playa"))



## Ejercicio 5 — **Bad Words**

### Objetivo
Escribe un programa que pida **una palabra** por teclado y diga si está en la lista de **palabras prohibidas** (`bad_words.txt`). La comparación debe ser **insensible a mayúsculas** .

##### Material proporcionado (NO modificar)
Se guarda el bloque que **carga** `bad_words.txt` en un `set` llamado `bad` (una palabra por línea):

def norm(s: str) -> str:
    return s.strip().lower()
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))	

palabra= input("Dame una palabra por favor: ")
if palabra=="" or " " in palabra: 
    print("Introduce una sola palabra (sin espacios).")
else: 
    pmodificada= norm(palabra)
    if pmodificada in bad: 
        print("NO CORRECTA")
    else: 
        print("CORRECTA")