#Ejercicio 4
def ultimoCaracter(dato):
    """Esta función revisa que tipo de dato se da como argumento para retornar una respuesta"""
    if type(dato) == str and len(dato) > 0:     #El len(dato) lo agrego para que no de error si se enrega un string vacio
        return dato[-1]
    else:
        return "Debo ser ejecutada con un string"

print(ultimoCaracter("python"))       #Responde "n"
print(ultimoCaracter(55))             #Responde "Debo ser ejecutada con un string"
print(ultimoCaracter(True))           #Responde "Debo ser ejecutada con un string"
print(ultimoCaracter(3.6))            #Responde "Debo ser ejecutada con un string"
print(ultimoCaracter(""))             #Responde "Debo ser ejecutada con un string"
