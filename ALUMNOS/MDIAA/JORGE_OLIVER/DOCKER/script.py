import sys

def pysum(a,b):
    return a + b

sys.argv[0]
sys.argv[1]

try: 
    num1 = float(sys.argv[1])
    num2 = float(sys.argv[2])
    resultado = num1 + num2
    print(f"Sum: {int(resultado)}")

except IndexError:
    print("Error: Tienes que pasar dos números. Ejemplo: docker run pysum 3 4")
except ValueError:
    print("Error: Ambos argumentos deben ser números.")