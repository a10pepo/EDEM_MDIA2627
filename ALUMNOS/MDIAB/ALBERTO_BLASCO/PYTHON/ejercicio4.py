def ultimoCaracter(a):
    if type(a) != str :
        return "Debe ser ejecutada con un string"
    else:
        return f"El último carácter es {a[-1]}"

palabra = input("Dime una palabra: ")
print(ultimoCaracter(palabra))