def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

entrada = input("Introduce una palabra: ").strip()

if entrada == "" or " " in entrada:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra = norm(entrada)
    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")

        