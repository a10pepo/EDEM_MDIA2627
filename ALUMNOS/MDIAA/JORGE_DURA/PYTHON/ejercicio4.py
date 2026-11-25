
def ultimoCaracter(palabra):
    if palabra == "":
        return "" 
    elif not isinstance(palabra, str):
        return 'Debo ser ejecutada con un string'
        
    return palabra[-1]

print(ultimoCaracter([1,2,3]))
print(ultimoCaracter("hola"))
print(ultimoCaracter(2))
print(ultimoCaracter(""))