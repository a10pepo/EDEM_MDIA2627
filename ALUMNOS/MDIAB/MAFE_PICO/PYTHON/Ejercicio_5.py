# Ejercicio 5 — Bad Words
# Objetivo
# Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas (bad_words.txt). La comparación debe ser insensible a mayúsculas .

# Material proporcionado (NO modificar)
# Se guarda el bloque que carga bad_words.txt en un set llamado bad (una palabra por línea):

# Cargar bad_words.txt (una palabra por línea; # = comentario)
# bad = set()
# with open("bad_words.txt", encoding="utf-8") as f:
#     for line in f:
#         w = line.strip()
#         if w:
#             bad.add(norm(w))
# Requisitos
# Normalización
# Crea la función norm(s: str) -> str que:

# convierte a minúsculas,
# quita espacios al inicio y al final.
# Entrada
# Pide al usuario una sola palabra con input().

# Validación
# Si la entrada está vacía o contiene espacios, muestra exactamente:

# Introduce una sola palabra (sin espacios).
# y termina el programa.

# Comprobación
# Normaliza la palabra introducida con norm(...).
# Comprueba si pertenece al conjunto bad cargado con el bloque proporcionado.
# Salida
# Si pertenece: imprime NO CORRECTA
# Si no pertenece: imprime CORRECTA
# Fichero de datos
# bad_words.txt contiene una palabra por línea.
# ejemplo archivo bad_words.txt:
# una por línea
# tonto idiota capullo

# Ejemplos para comprobar el ejercicio
# Entrada: IDIOTA → Salida: NO CORRECTA (si idiota está en el .txt)
# Entrada: saludo → Salida: CORRECTA
# Entrada: hola mundo → Salida: Introduce una sola palabra (sin espacios).

# 1. Normalización
def norm(s: str) -> str:
    return s.strip().lower()

# Material proporcionado (NO modificar)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# 2. Entrada
palabra = input("Introduce una palabra: ")

# 3. Validación (si está vacía o contiene espacios)
if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    # 4. Comprobación y 5. Salida
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")