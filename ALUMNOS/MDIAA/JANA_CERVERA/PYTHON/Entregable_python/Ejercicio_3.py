#1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.



def ultimoCaracter(texto):
    if type(texto) == str:
        return texto [-1]
    else:
        return "Debo ser ejecutada con un string"



print(ultimoCaracter(345))


