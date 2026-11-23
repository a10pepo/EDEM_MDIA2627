def ultimoCaracter(valor):
    if isinstance(valor, str):
        return valor[-1:]
    return "Debo ser ejecutada con un string"


print(ultimoCaracter("Hola"))
print(ultimoCaracter(123))
