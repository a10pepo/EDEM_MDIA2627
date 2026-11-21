# EJERCICIO 4

# 1.- Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 
# 2.- Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 

def ultimoCaracter(texto):
    if type(texto) != str:
        return "Debo ser ejecutada con un string"
    # Comprueba si el texto está vacío para devolver un string vacío
    # y evitar un error de índice al intentar acceder a texto[-1]
    if texto == "":
        return ""
    return texto[-1]
    
print(ultimoCaracter("hola"))
print(ultimoCaracter(12))
print(ultimoCaracter(""))



