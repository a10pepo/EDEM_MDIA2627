def ultimoCaracter(cadena):
    if type(cadena) != str or len(cadena) == 0:
        return "Debo ser ejecutada con un string"
    return cadena[-1]

print(ultimoCaracter("Hola"))
print(ultimoCaracter(5))
print(ultimoCaracter(""))
