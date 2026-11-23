def norm(s: str) -> str:
    m = s.lower()
    f = m.strip()
    return f

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una sola palabra: ")
if palabra.strip() == "" or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
else:
    norma = norm(palabra)
    if norma in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")