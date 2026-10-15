# Ejercicio 5 - Bad Words
def norm(s: str) -> str:
    """
    Convierte el texto a minúsculas y quita los espacios del inicio y del final.
    """
    return s.lower().strip()


# Cargar bad_words.txt (una palabra por línea; # = comentario)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una palabra: ")

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
