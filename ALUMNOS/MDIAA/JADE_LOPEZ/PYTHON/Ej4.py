#Ejercicio 4 : Bad words

#funcion norm

def norm(s:str)-> str:
     return s.strip().lower()

#Codigo proporcionado para leer el archivo de texto

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#pedir palabra

palabra=input("Dame una palabra:")

#validacion

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
else:
    palabra_normalizada = norm(palabra)
    
    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")