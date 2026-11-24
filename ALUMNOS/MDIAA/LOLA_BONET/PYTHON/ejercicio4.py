def ultimoCaracter(palabra):
    if not isinstance(palabra, str):
        return 'Debo ser ejecutada con un string'
    return palabra[-1]

print(ultimoCaracter("Marina"))
print(ultimoCaracter(123))