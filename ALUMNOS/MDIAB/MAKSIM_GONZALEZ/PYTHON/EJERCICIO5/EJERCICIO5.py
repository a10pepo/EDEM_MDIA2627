"""## Ejercicio 5 — **Bad Words**

### Objetivo
Escribe un programa que pida **una palabra** por teclado y diga si está en la lista de **palabras prohibidas** (`bad_words.txt`).  La comparación debe ser **insensible a mayúsculas** ."""
from ast import Continue

CONDICION = True
def norm(s: str) -> str:
    return s.strip().lower()


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

print("Bienvenido al programa de detección de palabras prohibidas.")

while CONDICION == True:
    #meto un bucle para que tenga mas chica y pueda introducir varias palabras
    palabra = input("Introduce una palabra o escribe 'salir' para terminar: ")


#aqui metemos la opcion de salir del bucle sino quieres continuar
    if palabra.lower() == 'salir':
        break

#si esta vacia o tiene espacios usamos el continue para que vuelva a pedir la palabra
    if not palabra or " " in palabra:
            print("Introduce una sola palabra (sin espacios).")
            continue


    elif norm(palabra) in bad:
            print("NO CORRECTA")
    else:
            print("CORRECTA")
    
    
 