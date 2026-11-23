def norm(s:str):
     return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

entrada= input("Introduce una palabra: ")
palabra=entrada.split()

if len(palabra) != 1:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_normalizada = norm(entrada)

    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA") 