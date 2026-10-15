#Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas (bad_words.txt).
#La comparación debe ser insensible a mayúsculas .

#REQUISITO 1: NORMALIZACIÓN
def norm(s: str) -> str:
    """Convierte a minúsculas y quita espacios al inicio y al final."""
    return s.strip().lower()


#MATERIAL PROPORCIONADO (NO modificar): Cargar bad_words.txt (una palabra por línea; # = comentario)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


#REQUISITO 2: ENTRADA
palabra = input("Dime una palabra")
print(f"Hola, la palabra es {palabra}")

#REQUISITO 3: VALIDACIÓN
if not palabra:
    print("Introduce una sola palabra (sin espacios).")
elif " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    #REQUISITO 4 Y 5: COMPROBACIÓN Y SALIDA
    palabra_normalizada = norm(palabra)
    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")