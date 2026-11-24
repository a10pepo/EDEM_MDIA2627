

def ultimoCaracter(texto):
   
    if isinstance(texto, str):
        if len(texto) > 0:
            return texto[-1]
        else:
            return ""
    else:
        return "Debo ser ejecutada con un string"


# Ejemplos de uso
print(ultimoCaracter("Marina"))
print(ultimoCaracter(123))
