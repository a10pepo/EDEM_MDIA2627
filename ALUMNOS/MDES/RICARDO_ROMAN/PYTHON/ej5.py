# EJ5
def norm(s: str) -> str:
    """
    Normaliza la cadena: elimina espacios al principio y al final, y pasa a minúsculas.
    Argumentos:
        s: str -> cadena a normalizar
    Returns:
        str -> cadena normalizada
    """
    return s.strip().lower()

# Cargamos las palabras
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


palabra = input("Introduce una palabra: ")


# Validacion
if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
elif norm(palabra) in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")
