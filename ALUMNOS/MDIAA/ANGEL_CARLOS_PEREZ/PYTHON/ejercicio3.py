def ultimoCaracter(palabra):
    if type(palabra)==str:
        return palabra[-1]
    else:
        return "Debo ser ejecutada con un string"


print(ultimoCaracter("Hola"))
print(ultimoCaracter(8))