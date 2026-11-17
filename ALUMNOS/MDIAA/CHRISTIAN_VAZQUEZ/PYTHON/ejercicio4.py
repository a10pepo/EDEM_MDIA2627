def ultimoCaracter(palabra):
    if type(palabra) == str:
        return f"Último carácter: {palabra[-1]}"
    else:
        return "Debo ser ejecutada con un string"

print(ultimoCaracter("queso"))
print(ultimoCaracter(5.6))