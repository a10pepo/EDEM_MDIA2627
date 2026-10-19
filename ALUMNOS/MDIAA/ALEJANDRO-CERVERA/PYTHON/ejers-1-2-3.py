# Ejercicio 1

# Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”

variable = "Marina de Empresas 2025"

# Muestra por consola la longitud de la variable

print(len(variable))

# Utilizando esa variable muestra por consola la primera letra.

print(variable[0])

# Ejercicio 2

# Define una variable festivo que sea de tipo booleano.

festivo = False

# Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”

if festivo:
    print('Hoy es fiesta voy a echarme una siesta!!')
else:
    print('No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)')

# Ejercicio 3

# Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.

def ultimoCaracter (input):
    return input[-1]

# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.

def ultimoCaracter (input):
    if type(input) == str:
        return input[-1]
    else:
        return 'Debo ser ejecutada con un string'