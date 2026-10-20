# EJ4
def ultimoCaracter(cadena: str) -> str:
    if not isinstance(cadena, str):
        return "Debo ser ejecutada con un string"
    return cadena[-1]

print(ultimoCaracter("Marina"))
print(ultimoCaracter(5))
