# Entregable Python - Adrián Lázaro

# Ejercicio 1

print("--- Ejercicio 1 ---")

texto = "Marina de Empresas 2025"

# Longitud de la variable
print(len(texto))

# Primera letra
print(texto[0])

# Ejercicio 2
# ------------------------------------------------------------
print("\n--- Ejercicio 2 ---")
 
festivo = True
 
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# Ejercicio 4
# ------------------------------------------------------------
print("\n--- Ejercicio 4 ---")
 
def ultimoCaracter(texto):
    if type(texto) == str:
        return texto[-1]
    else:
        return 'Debo ser ejecutada con un string'

# Ejercicio 5 - Bad Words

def norm(s: str) -> str:
    """Convierte a minúsculas y quita espacios al inicio y al final."""
    return s.strip().lower()


# Cargar bad_words.txt (una palabra por línea; # = comentario)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Entrada
palabra = input("Introduce una palabra: ")

# Validación
if palabra.strip() == "" or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    # Comprobación y salida
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
 
