# ==========================================
# EJERCICIO 1
# ==========================================
print("--- Ejercicio 1 ---")

var = "Marina de Empresas 2025"

print("Longitud de la variable:", len(var))
print("Primera letra:", var[0])
print()


# ==========================================
# EJERCICIO 2
# ==========================================
print("--- Ejercicio 2 ---")

festivo: bool = True

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")
print()


# ==========================================
# EJERCICIO 4
# ==========================================
print("--- Ejercicio 4 ---")

def ultimoCaracter(palabra: str) -> str:
    """Devuelve el último carácter de un string o un mensaje de error si no es string."""
    if type(palabra) == str:
        return palabra[-1]
    else:
        return "Debo ser ejecutada con un string"

# Pruebas de ejecución del Ejercicio 4
print("Prueba con 'Python':", ultimoCaracter("Python"))
print("Prueba con un número:", ultimoCaracter(123))
print()


# ==========================================
# EJERCICIO 5: Bad Words
# ==========================================
print("--- Ejercicio 5 ---")

def norm(s: str) -> str:
    """Normaliza un string convirtiéndolo a minúsculas y eliminando espacios."""
    return s.lower().strip()

# 1. Carga de datos
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# 2. Entrada del usuario
word = input("Introduce una sola palabra: ")

# 3. Validación y comprobación
if not word or " " in word:
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(word) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
print()