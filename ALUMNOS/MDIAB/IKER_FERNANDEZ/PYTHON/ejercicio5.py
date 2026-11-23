def norm(s: str) -> str:
    """Pasa el texto a minúsculas y quita los espacios del principio y del final."""
    texto: str = s.lower()

    inicio: int = 0
    while inicio < len(texto) and texto[inicio] == " ":
        inicio += 1

    fin: int = len(texto) - 1
    while fin >= inicio and texto[fin] == " ":
        fin -= 1

    resultado: str = ""
    posicion: int = inicio
    while posicion <= fin:
        resultado += texto[posicion]
        posicion += 1

    return resultado


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


def comprobar(palabra: str) -> str:
    """Devuelve el mensaje que corresponde a la palabra introducida."""
    palabra = norm(palabra)
    if palabra == "" or " " in palabra:
        return "Introduce una sola palabra (sin espacios)."
    elif palabra in bad:
        return "NO CORRECTA"
    else:
        return "CORRECTA"


print(comprobar(input("Introduce una palabra: ")))