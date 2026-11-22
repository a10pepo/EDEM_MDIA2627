### EJERCICIO 1
print("Ejercicio 1:")

mde = "Marina de Empresas 2025"

print(len(mde))
print(mde[0])

### EJERCICIO 2
print("Ejercicio 2:")

festivo = True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

### EJERCICIO 4
print("Ejercicio 4:")

def ultimoCaracter(texto):
    if type(texto) == type("hola"):
        return texto[-1]
    else:
        return "Debo ser ejecutada con un string"

print(ultimoCaracter("carla"))
    



