def ultimoCaracter(texto):
    if not isinstance(texto, str):
        return "Debo ser ejecutada con un string"
    return texto[-1]


print(ultimoCaracter("Marina de Empresas"))
print(ultimoCaracter(2025))