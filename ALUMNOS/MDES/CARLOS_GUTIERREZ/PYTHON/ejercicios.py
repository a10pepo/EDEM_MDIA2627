

# EJERCICIO 1
mde: str = "Marina de Empresas 2025"
print(f"Longitud de la variable: {len(mde)} \n"
      f"Primera letra de la variable: {mde[0]}")

# EJERCICIO 2
festivo: bool = True
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de python:)")

# EJERCICIO 3(4)
def ultimo_caracter(secuencia: str):
    if type(secuencia) != str:
        return "Debo ser ejecutado con un string"
    else: 
        return secuencia[-1]
print(ultimo_caracter(3344343))

# EJERCICIO 4(5)
def norm(s: str)->str:
    return s.lower().strip()

palabra_introducida = input("Introduce una palabra: ")

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

if not palabra_introducida.strip() or " " in palabra_introducida.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_normalizada = norm(palabra_introducida)
    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else: 
        print("CORRECTA")
    

