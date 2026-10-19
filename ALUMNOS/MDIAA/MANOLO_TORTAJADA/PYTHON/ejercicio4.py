# 1. Crea la función ultimoCaracter debe recibir un tipo string y 
# devolver un string con el último carácter.
from warnings import catch_warnings


def ultimoCaracter(tipo):
    if isinstance(tipo, str):
        return tipo[-1]
    return 'Debo ser ejecutada con un string'


# 2. Si la función no recibe un dato tipo string debe devolver el 
# string 'Debo ser ejecutada con un string'.
print('Ahora vamos a mostrar el último caracter de "Manolo"')
print(ultimoCaracter("Manolo"))  # o
print('Ahora vamos a llamar a la función con un número')
print(ultimoCaracter(1242))      # Debo ser ejecutada con un string
