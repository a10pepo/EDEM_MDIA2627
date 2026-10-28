#Construir un script en python que acepte dos 
#números como parámetros e imprima el resultado de la suma

a= float(input("Dame el primer numero:"))
b=float(input("Dame el segundo numero:"))

resultado = a + b

#Para que me de un numero entero
if resultado.is_integer():
    resultado = int(resultado)

print(resultado)

