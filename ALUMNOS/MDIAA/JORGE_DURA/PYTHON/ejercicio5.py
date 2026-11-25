def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra_usuario = input("Introduce la palabra a comprobar: ")

if not palabra_usuario or " " in palabra_usuario:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_comprobar = norm(palabra_usuario)
    
    if palabra_comprobar in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")