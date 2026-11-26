# ==========================================
# EJERCICIO 1
# ==========================================
print("=== EJERCICIO 1 ===")

texto: str = "Marina de Empresas 2025"

print(f"Longitud: {len(texto)}")
print(f"Primera letra: {texto[0]}")



print()
# ==========================================
# EJERCICIO 2
# ==========================================
print("=== EJERCICIO 2 ===")

festivo: bool = True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")



print()
# ==========================================
# EJERCICIO 4
# ==========================================
print("=== EJERCICIO 4 ===")

def ultimoCaracter(texto: str) -> str:
    if type(texto) == str:  #if isinstance(texto, str):
        return texto[-1]
    return "Debo ser ejecutada con un string"

# Ejemplos
print(ultimoCaracter("Sergio Mancebo"))
print(ultimoCaracter(12345))



print()
# ==========================================
# EJERCICIO 5
# ==========================================
print("=== EJERCICIO 5 ===")

# Función de normalización
def norm(s: str) -> str:
    return s.strip().lower()

# Cargar bad_words.txt (una palabra por línea)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Entrada por teclado
palabra: str = input("Introduce una palabra por teclado: ")

# Validación
if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    # Comprobación y salida
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")