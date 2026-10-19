def ultimoCaracter(a):
    if type(a)==str:
        return a[-1]
    else:
        return "Debo ser ejecutada con un string"
print(ultimoCaracter("Hola"))