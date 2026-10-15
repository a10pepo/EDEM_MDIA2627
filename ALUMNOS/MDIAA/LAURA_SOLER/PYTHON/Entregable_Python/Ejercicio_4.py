#Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
#Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.
def ultimoCaracter(palabra):
    if type(palabra) == str:
        return palabra[-1]
    else:
        return "Debo ser ejecutada con un string"

print(ultimoCaracter("Python"))
print(ultimoCaracter(20))