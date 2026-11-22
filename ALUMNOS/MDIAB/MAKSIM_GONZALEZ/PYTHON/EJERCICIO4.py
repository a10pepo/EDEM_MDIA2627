"""## Ejercicio 4
1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 

2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. """

def ultimoCaracter(cadena):
    if type(cadena) == str:
        return cadena[-1]
    else:
        return 'Debo ser ejecutada con un string'

#no hago mas código ya que al usar input() no puedo hacer pruebas de la función, ya que al ser un input siempre devuelve un string, y no puedo probar el caso en el que no se le pasa un string.