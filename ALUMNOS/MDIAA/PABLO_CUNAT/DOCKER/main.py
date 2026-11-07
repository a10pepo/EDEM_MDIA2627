import sys

def suma_elementos (a, b):
    return a + b

arg_1 = int(sys.argv[1])
arg_2 = int(sys.argv[2])

print(f"Suma: {suma_elementos(arg_1, arg_2)}")