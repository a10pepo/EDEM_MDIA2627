
## Ejercicio 4
# Ejercicio 4

def ultimoCaracter(texto):
    # 2. Si no recibe un string, devuelve el mensaje de error
    if not isinstance(texto, str):
        return 'Debo ser ejecutada con un string'
    # 1. Devuelve el último carácter (cadena vacía si el string está vacío)
    return texto[-1:]


# Pruebas
print(ultimoCaracter("Python"))    # n
print(ultimoCaracter("Hola!"))     # !
print(ultimoCaracter(123))         # Debo ser ejecutada con un string
print(ultimoCaracter(["a", "b"]))  # Debo ser ejecutada con un string
