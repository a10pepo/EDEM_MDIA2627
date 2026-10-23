# Tarea Python
# Ejercicio 1:
# 1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025” 
info = "Marina de Empresas 2025"
# 2. Muestra por consola la longitud de la variable
print(len(info))
# 3. Utilizando esa variable muestra por consola la primera letra.
print(info[0])

# Ejercicio 2
# 1. Define una variable festivo que sea de tipo booleano. 
festivo: bool = True
print(festivo)

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola 
# “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola 
# “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”
if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


# Ejercicio 4 (3)
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 
# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.
def ultimoCaracter(palabra):
    if type(palabra) == str:
        return palabra[-1]
    else:
        return "Debo ser ejecutada con un string"
print(ultimoCaracter("tenis"))
print(ultimoCaracter(2))

# Ejercicio 5 — **Bad Words**
# Objetivo
# Escribe un programa que pida **una palabra** por teclado y diga si está en la lista de **palabras prohibidas** (bad_words.txt). La comparación debe ser **insensible a mayúsculas**.
# Material proporcionado (NO modificar)
# Se guarda el bloque que carga (bad_words.txt) en un set llamado bad (una palabra por línea)

# Cargar bad_words.txt (una palabra por línea; # = comentario)

# bad = set()
# with open("bad_words.txt", encoding="utf-8") as f:
#     for line in f:
#         w = line.strip()
#         if w:
#             bad.add(norm(w))
#
# Requisitos
#
# Normalización
# Crea la función `norm(s: str) -> str` que:
# - convierte a minúsculas,
# - quita espacios al inicio y al final.
def norm(s: str) -> str:
    s = s.lower()

    for caracter in s:
        if s == "":
            return s
        if s[0] == " ":
            s = s[1:len(s)]

    for caracter in s:
        if s == "":
            return s
        if s[-1] == " ":
            s = s[0:len(s) - 1]

    return s

# Entrada
# Pide al usuario **una sola palabra** con `input()`.
procedimiento = True
word = input("Introduce una sola palabra: ")
# Validación
# Si la entrada está vacía o contiene espacios, muestra exactamente:
check = word.replace(" ", "")
if word == "" or word != check:
# Introduce una sola palabra (sin espacios).
#
# y termina el programa.
    print("Introduce una sola palabra (sin espacios).")
    procedimiento = False
if procedimiento == True:
    word = norm(word)
    bad = set()
    with open("bad_words.txt", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                bad.add(norm(w))

### Comprobación
# - Normaliza la palabra introducida con `norm(...)`.
# - Comprueba si pertenece al conjunto `bad` cargado con el bloque proporcionado.

### Salida
# - Si pertenece: imprime **NO CORRECTA**
# - Si no pertenece: imprime **CORRECTA**
    if word in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

### Fichero de datos
# - `bad_words.txt` contiene **una palabra por línea**.

### ejemplo archivo bad_words.txt:
### una por línea 
#tonto
#idiota
#capullo


### Ejemplos para comprobar el ejercicio

##### Entrada: IDIOTA → Salida: NO CORRECTA (si idiota está en el .txt)

##### Entrada: saludo → Salida: CORRECTA

##### Entrada: hola mundo → Salida: Introduce una sola palabra (sin espacios).