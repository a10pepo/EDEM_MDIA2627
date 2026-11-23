# Ejercicio 5 — Bad Words
# Objetivo
# Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas (bad_words.txt). 
# La comparación debe ser insensible a mayúsculas.

def norm(s: str) -> str:
        norm_word = s.lower().strip()
        return norm_word

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

word = input("Introduce una sola palabra")

if word == "" or " " in word:
    print("Introduce una sola palabra (sin espacios).")
else:
    norm_word = norm(word)
    if norm_word in bad:
        print ("NO CORRECTA")
    else:
        print ("CORRECTA")


