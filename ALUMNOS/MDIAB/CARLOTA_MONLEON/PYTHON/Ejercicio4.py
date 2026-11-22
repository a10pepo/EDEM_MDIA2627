# Ejercicio 4
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.

def ultimoCaracter (entrada):
    if type(entrada) != str:
        return("Debo ser ejecutada con un string")
    else:
        return(entrada[-1])

print(ultimoCaracter("Carlota"))
print(ultimoCaracter(23))