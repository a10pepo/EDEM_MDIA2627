def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una palabra: ")

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")

else:
    palabra = norm(palabra)
    
    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")