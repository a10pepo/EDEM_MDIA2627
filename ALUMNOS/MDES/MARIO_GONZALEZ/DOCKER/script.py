import sys

def suma(a,b):
    entero1 = int(a)
    entero2 = int(b)
    return entero1 + entero2

print(f"Sum: {suma(sys.argv[1],sys.argv[2])}")