# Ejercicio 5 — Bad Words

def norm(s: str) -> str:
    """Convierte a minúsculas y quita espacios al inicio y al final."""
    return s.lower().strip()


# Cargar bad_words.txt (una palabra por línea; # = comentario)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Entrada
entrada = input("Introduce una palabra: ")

# Validación: si está vacía o tiene algún espacio, mensaje y fin
if not entrada or " " in entrada:
    print("Introduce una sola palabra (sin espacios).")
else:
    # Comprobación
    palabra = norm(entrada)
    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")