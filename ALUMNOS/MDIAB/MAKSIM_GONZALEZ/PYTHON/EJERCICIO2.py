"""## Ejercicio 2
1. Define una variable festivo que sea de tipo booleano. 

2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” """

festivo = False

#si quiero que me pregunte a mi si es festivo o no, puedo hacer lo siguiente:
# festivo = input("¿Es festivo hoy? (si/no): ")
# if festivo.lower() == "si":
#     festivo = True    
# else: 
#     festivo = False

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")