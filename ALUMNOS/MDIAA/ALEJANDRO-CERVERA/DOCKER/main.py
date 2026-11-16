import sys

def suma(num1, num2):
    return num1 + num2

try:
    numero1 = float(sys.argv[1])
    numero2 = float(sys.argv[2])
    print(f'La suma de {numero1} y {numero2} es igual a {suma(numero1, numero2)}.')
except (ValueError, IndexError):
    print('Error: debes introducir dos números.')
