def norm(s: str) -> str:
    return s.strip().lower()


palabra = input()

if not palabra or any(caracter.isspace() for caracter in palabra):
    print("Introduce una sola palabra (sin espacios).")
    raise SystemExit

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

if norm(palabra) in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")
