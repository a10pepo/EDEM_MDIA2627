import sys

if len(sys.argv) != 3:
    print("Uso: python suma.py <numero1> <numero2>")
    sys.exit(1)

try:
    a = float(sys.argv[1])
    b = float(sys.argv[2])
except ValueError:
    print("Error: los dos argumentos deben ser números")
    sys.exit(1)

print(f"{a} + {b} = {a + b}")
