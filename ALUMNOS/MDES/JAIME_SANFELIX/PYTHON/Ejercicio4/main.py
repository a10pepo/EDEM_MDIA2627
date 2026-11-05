def norm(s: str) -> str:
    minuscula = s.lower();
    sinEspacios = str(minuscula).strip();
    return sinEspacios;

print("Introduce una palabra ");
palabra = input();
norm(palabra);


bad = set()
with open('bad_words.txt', encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
            print(bad);

if(norm(palabra) in bad):
    print("No correcta");
elif(norm(palabra) not in bad):
    print("Correcta")