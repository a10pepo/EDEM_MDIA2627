def ultimoCaracter(texto) -> str:
    if not isinstance(texto, str):
        return "Debo ser ejecutada con un string"

    return texto[-1:]
