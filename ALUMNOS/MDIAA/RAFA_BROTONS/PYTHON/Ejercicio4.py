def ultimo_caracter (texto):
    if type(texto) == str:
        return texto[-1]
    else:
        return "Debo ser ejecutada con un string"

print(ultimo_caracter("Python"))
print(ultimo_caracter(123))
