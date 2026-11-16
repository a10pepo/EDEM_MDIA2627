def ultimoCaracter(palabra):
    if(type(palabra) != str):
        return "Debo ser ejecutada con un string";
    else:
        return palabra[-1];
    
print(ultimoCaracter("plato"))