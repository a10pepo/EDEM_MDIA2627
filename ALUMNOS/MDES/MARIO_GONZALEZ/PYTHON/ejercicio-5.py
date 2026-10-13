palabra_teclado : str = input("Introduce una palabra: ")

def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

if not palabra_teclado or " " in palabra_teclado:
    print("Introduce una sola palabra (sin espacios)")
elif norm(palabra_teclado) in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")