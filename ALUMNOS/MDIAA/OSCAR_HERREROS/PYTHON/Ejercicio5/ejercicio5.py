#Normalización de palabras
def norm(letra):
    return letra.strip().lower()

#Estructura de carga de "bad_words.txt"
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#Entrada de la palabra        
palabra = input("Introduce una sola palabra: ")

if len(palabra) == 0 or len(palabra.split()) > 1 or len(palabra.split()) == 0:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra)
    if palabra_norm in bad:
        print(f"NO CORRECTA ({palabra}) se encuentra en el .txt")
    else:
        print(f"CORRECTA ({palabra}) no se encuentra en el .txt")
    
