# Ejercicio 5 — Bad Words

# Normalización: minúsculas y sin espacios al inicio/final.
# Debe definirse ANTES del bloque de carga, porque ese bloque la usa.
def norm(s: str) -> str:
    return s.strip().lower()


# --- Bloque proporcionado (NO modificar) ---
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
# -------------------------------------------

# Entrada
palabra = input("Introduce una palabra: ").strip()

# Validación: vacía o con espacios
if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    # Comprobación y salida
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")