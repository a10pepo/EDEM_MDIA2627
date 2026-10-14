# EJ1
############################################
nombre: str = "Marina de Empresas 2025"
print(len(nombre))
print(nombre[0])
############################################

# EJ2
############################################
festivo: bool = True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")
############################################



# EJ4
############################################
def ultimo_caracter(cadena: str) -> str:
    if type(cadena) != str:
        return "Debo ser ejecutada con un string"
    return cadena[-1]
############################################


# EJ5
############################################
palabra = input("Introduce una palabra: ")

def norm(s: str) -> str:
    # quitar espacios al inicio y al final y converti a minusculas
    return s.strip().lower()


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
            

############################################