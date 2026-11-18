import os


def norm(s: str) -> str:
    return s.strip().lower()


palabra = input("Escribe una palabra: ")
partes = palabra.split()

if not partes or palabra != partes[0]:
    print("Introduce una sola palabra (sin espacios).")
else:
    carpeta_ejercicio = os.path.dirname(os.path.abspath(__file__))
    os.chdir(carpeta_ejercicio)

    bad = set()
    with open("bad_words.txt", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                bad.add(norm(w))

    bad = {w for w in bad if not w.startswith("#")}

    if norm(palabra) in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
