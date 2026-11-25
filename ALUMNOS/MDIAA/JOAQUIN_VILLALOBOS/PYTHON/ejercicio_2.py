#Ejercicio 2

def que_hacer(bol):
    if bol:                 #No es necesario hacer un == True, ya que eso se da por sentado.
        print("Hoy es fiesta voy a echarme una siesta!!")
    else:
        print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


festivo = False             #Variable tipo Boolean
que_hacer(festivo)          #Responde que no hay fiesta, por ser False

festivo = True              #Variable tipo Boolean
que_hacer(festivo)          #Responde que SI hay fiesta, por ser True