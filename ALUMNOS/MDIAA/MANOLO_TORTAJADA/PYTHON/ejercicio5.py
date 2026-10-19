# Ejercicio 5 — Bad Words
# Objetivo
# Escribe un programa que pida una palabra por teclado y 
# diga si está en la lista de palabras prohibidas (bad_words.txt). 
# La comparación debe ser insensible a mayúsculas .

# Requisitos
# Normalización
def norm(s: str):
    """

    Args:
        s (str): 

    Returns:
        string: Devuelve el string s normalizado (en minúsculas y sin espacios)
    """
    return s.lower().strip()

# Cargar bad_words.txt (una palabra por línea; # = comentario)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Entrada
# Pide al usuario una sola palabra con input().
# Lo dejo ya normalizado
userInput = input('Escribe una sola palabra ')

# Validación
# Si la entrada está vacía o contiene espacios, muestra exactamente:
# Con el not .strip comprueba si está vacio
# Si la long != 1, ha puesto más de una palabra
if not userInput or " " in userInput:
    print(f'Introduce una sola palabra (sin espacios).')
    exit()

# Comprobación
# Normaliza la palabra introducida con norm(...).
userInputnorm = norm(userInput)

# Comprueba si pertenece al conjunto bad cargado con el bloque proporcionado.
# Salida
if userInputnorm in bad:
    # Si pertenece: imprime NO CORRECTA
    print('NO CORRECTA') 
else:
    # Si no pertenece: imprime CORRECTA
    print('CORRECTA') 


