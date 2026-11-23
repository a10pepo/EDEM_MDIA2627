def ultimoCaracter(texto):
    if isinstance(texto, str):
        return texto[-1]
    else:
        return 'Debo ser ejecutada con un string'


print(ultimoCaracter("Python"))
print(ultimoCaracter(25))
