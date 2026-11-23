def ultimoCaracter(texto):
    if type(texto) == str and len(texto) > 0:
         return texto[-1]
    else:
        return "Debo ser ejecutada con un string"
  
texto = input("Dame un texto: ")
print(ultimoCaracter(texto))

