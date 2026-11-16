import sys

def suma(num1: int, num2: int):
    return num1 + num2

a = int(sys.argv[1])
b = int(sys.argv[2])

print(f"Sum: {suma(a, b)}")