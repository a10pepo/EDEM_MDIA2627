#Ejercicio 3
# Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.


def ultimoCaracter(palabra):
    if type(palabra) != str:
        return "Debo ser ejecutada con un string"
    else:
        return palabra[-1]

print(ultimoCaracter("Hola"))
print(ultimoCaracter(300))