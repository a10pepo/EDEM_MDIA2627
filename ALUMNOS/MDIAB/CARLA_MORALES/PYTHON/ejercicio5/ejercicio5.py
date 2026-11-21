# EJERCICIO 5

# 1.- Creamos la función de normalización

def norm(s: str) -> str:
    return s.strip().lower()

# 2.- Cargamos las palabras del fichero bad_words.txt

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# 3.- Pedimos una palabra

palabra = input("Introduce una palabra: ")

# 4.- Validación

# 5.- Si la entrada está vacía o contiene espacios, mostramos el mensaje:
# "Introduce una sola palabra (sin espacios)."

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    # 6.- Normalizamos la palabra introducida 
    palabra = norm(palabra)

    # 7.- Comprobamos si pertenece al conjunto bad
    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

