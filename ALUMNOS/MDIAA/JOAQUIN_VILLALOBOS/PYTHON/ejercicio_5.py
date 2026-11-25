#Ejercicio 4
def norm(s: str):
    """normalización de palabras"""
    return s.strip().lower()       #strip() quita espacios de las esquinas y lower() transforma todo a minúsculas

bad = set()         
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

def comprobacion_input(palabra):
    """revisa que la palabra ingresada sea válida. De ser así, ve si forma parte de la 'lista negra' y da una respuesta."""
    if " " in palabra or palabra.strip() == "" or len(palabra.split()) != 1:
        #buscamos saber si el input ingresado tiene espacios en los extremos, en el medio, si hay tabulacion de por medio o si alguien envio un input vacio
        print("Introduce una sola palabra (sin espacios).")
        return
    palabra_a_comparar = norm(palabra)
    if palabra_a_comparar in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

mala_palabra = input("Dime una mala palabra: ")
comprobacion_input(mala_palabra)