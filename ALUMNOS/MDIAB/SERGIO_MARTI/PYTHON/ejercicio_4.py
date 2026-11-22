# ## Ejercicio 4
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 
def ultimoCaracer(texto:str) -> str:
    return texto[-1]

# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 
def ultimoCaracter(texto):
    if texto != str:
        print("Debo ser ejecutada con un string")
        
    return(texto[-1])
