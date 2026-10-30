import sys

# Definimos la función de la suma:
def sumar(a,b):
    return a + b

# docker run pysum 3 4:
num1 = int(sys.argv[1])
num2 = int(sys.argv[2])

# Llamar a la función:
print(f'Sum: {sumar(num1, num2)}')
