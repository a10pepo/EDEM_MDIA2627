## Ejercicio 4
def ultimoCaracter(x):
    if type(x) == str:
        return(x[-1])
    else:
        return("Debo ser ejecutada con un string")

print(ultimoCaracter("Ciao"))
print(ultimoCaracter(44))