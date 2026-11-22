def norm(texto: str) -> str:
    return texto.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

texto = input("Introduce una palabra (sin espacios): ")

if texto == "" or " " in texto:
    print("Introduce una sola palabra (sin espacios): ")
else: 
    palabra = norm(texto)

    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")