# Ejercicio 1

frase = "Marina de Empresas 2025"

print(len(frase))
print(frase[0])

# Ejercicio 2

esFestivo = True

if esFestivo:
    print("Hoy es fiesta voy a echarme una siesta")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# Ejercicio 4

def ultimoCaracter(str: str) -> str:
    try:
        return frase[-1]
    except:
        return "Debo ser ejecutada con un string"

# Ejercicio 5

