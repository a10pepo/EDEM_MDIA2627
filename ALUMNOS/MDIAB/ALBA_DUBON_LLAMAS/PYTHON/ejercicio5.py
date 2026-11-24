def norm(s: str) -> str:
    return s.lower().strip()

from pathlib import Path
ruta = Path(__file__).resolve().parent / "bad_words.txt"
bad = set()
with open(ruta, encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


palabra = input("Introduce una palabra: ")

if not palabra or any(caracter.isspace() for caracter in palabra):
    print("Introduce una sola palabra (sin espacios).")

else:
    palabra = norm(palabra)

    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")