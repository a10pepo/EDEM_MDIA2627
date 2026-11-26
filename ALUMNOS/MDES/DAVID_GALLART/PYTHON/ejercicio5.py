def norm(s: str) -> str:
     return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

texto = input("Dame un texto: ")

if len(texto) <= 0 or " " in texto:
    print("Introduce una sola palabra (sin espacios).")
else:
    texto = norm(texto)
    if texto in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
