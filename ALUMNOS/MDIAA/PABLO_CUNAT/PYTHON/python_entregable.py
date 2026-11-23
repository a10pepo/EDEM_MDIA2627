# --------------------------------------  Ejercicio 1 ---------------------------------------------------------------
# 1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”

texto_1="Marina de Empresas 2025"

# 2. Muestra por consola la longitud de la variable

print(len(texto_1))

# Utilizando esa variable muestra por consola la primera letra.

print(texto_1[0])

# --------------------------------------  Ejercicio 2 ---------------------------------------------------------------

# 1. Define una variable festivo que sea de tipo booleano.

festivo:bool=True

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


# --------------------------------------  Ejercicio 4 ---------------------------------------------------------------

# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.

def ultimoCaracter(s: str) -> str:
    return s[-1]



# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.

def ultimoCaracter(s: str) -> str:
    if not isinstance(s, str):
        return 'Debo ser ejecutada con un string'
    return s[-1]    


# --------------------------------------  Ejercicio 5 — Bad Words ----------------------------------------------------

#primero creamos función de normalizacion con def, en teoría, se debería recibir una palabra en formato string y devolvernos otro string
#a continuación, con strip quitamos cualquier espacio que pueda haber al principio o final y con lower hacemos que sea todo lowercase.
def norm(s: str) -> str:
    return s.strip().lower()

#en este bloque de código se crea un conjunto set vacío con las palabras del .txt una vez han pasado por el bucle for.
#Se abre el archivo con codificación UTF-8 y dentro del bucle se leen las palabras, eliminando los espacios al principio o al final

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#empleamos input para hacer que el usuario intruduzca una palabra
palabra = input("Introduce una palabra: ")

#if not palabra se usa para que si no se escribe nada, aparezca el mensaje de abajo, o si hay espacio o si hay un número
#si no, la palabra escrita se normaliza y si la palabra está en el set anterior, se obtiene no correcta y sino, correcta.
if not palabra or " " in palabra or palabra.isdigit():
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra = norm(palabra)

    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")



