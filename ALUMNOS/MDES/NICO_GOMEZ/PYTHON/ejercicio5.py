def norm(s : str) -> str:
    s_min = s.lower()
    s_norm = s_min.strip()
    return s_norm


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Escribe una palabra")

if palabra == "":
    print("Introduce una sola palabra (sin espacios).")
elif " " in norm(palabra):
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")