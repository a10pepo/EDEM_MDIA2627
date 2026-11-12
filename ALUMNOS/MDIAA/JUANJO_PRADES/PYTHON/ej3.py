def ultimoCaracter(texto):
    if type(texto) != str:
        return 'Debo ser ejecutada con un string'
    return texto[-1]