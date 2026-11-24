## Ejercicio 5
def norm(s: str) -> str:
    return s.strip().lower()

#norm recibe una string (s) y devuelve una string sin espacios y en minusculas


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#Set vacio que se llena en bad_words.txt


palabra = input("Escribe una palabra: ")

#Pide una palabra al ususario


if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra)
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

#La palabra del usuario puede ser CORRECTA, si no està en bad_words.txt, NO CORRECTA, si està en bad_words.txt, o no se acepta, si tiene espacios o es vacia.