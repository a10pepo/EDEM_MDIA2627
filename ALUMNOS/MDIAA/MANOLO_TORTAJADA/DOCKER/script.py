import sys

def getNumeros():
    return sys.argv[1:] # 1: cojo todo menos la primera pos

def sumaNumeros():
    numeros = getNumeros()
    suma = 0
    for numero in numeros:
        # Casteamos xq vienen en string. 
        # Suponemos que el user pone números enteros :)
        suma += int(numero) 
    return suma

print(f'Sum: {sumaNumeros()}')