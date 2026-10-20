## Ejercicio 5
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

y = input("Escribe una palabra: ")

def norm(s: str) -> str:
    return s.strip().lower()
    
    '''
    s.strip() = elimina espacios y tabs
    .lower() = convierte todos en letras minuscolas
    '''

print(y)