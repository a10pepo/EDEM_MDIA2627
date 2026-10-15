# Ejercicio 4
def ultimoCaracter(texto):
    """
    Recibe un string y devuelve su último carácter.
    Si no recibe un string, devuelve un mensaje de aviso.
    """
    if isinstance(texto, str):
        return texto[-1]
    else:
        return 'Debo ser ejecutada con un string'


print(ultimoCaracter("Python"))  # n
print(ultimoCaracter(25))        # Debo ser ejecutada con un string
