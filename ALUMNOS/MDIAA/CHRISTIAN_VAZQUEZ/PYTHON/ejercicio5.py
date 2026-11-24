def norm(s:str):
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Dame una palabra: ")

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_trans = norm(palabra)
    if palabra_trans in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")