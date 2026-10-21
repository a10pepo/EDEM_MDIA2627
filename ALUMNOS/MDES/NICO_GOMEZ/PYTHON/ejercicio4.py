def ultimoCaracter(palabra : str) -> str:
    try:
        return palabra[-1]
    except:
        print("Debo ser ejecutada con un string")

# print(ultimoCaracter("Hola"))
# print(ultimoCaracter(2))