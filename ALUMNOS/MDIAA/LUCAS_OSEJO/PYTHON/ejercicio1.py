# Ejercicio 1
# Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
variable1 = "Marina de Empresas 2025"

# Muestra por consola la longitud de la variable
print(len(variable1))

# Utilizando esa variable muestra por consola la primera letra.
print(variable1[0])
# Ejercicio 2
# Define una variable festivo que sea de tipo booleano.
festivo: bool = True
# Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”
if festivo == True:
    print("Hoy es fiesta, voy a echarme una siesta!")
else:
    print("No pasa nada porque tengo que hacer el entregable de Python")
# Ejercicio 4
# Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
def ultimoCaracter(texto):
    return (texto[-1])
print(ultimoCaracter("Lucas"))
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.

def ultimoCaracter(texto):
    if type(texto) != str: 
        return f"Debo ser ejecutada con un string"
    else:
        return (texto[-1])

print (ultimoCaracter(34))