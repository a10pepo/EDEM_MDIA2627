import sys

if len(sys.argv) != 3:
    print("Uso: docker run pysum <num1> <num2>")
    sys.exit(1)

try:
    a = float(sys.argv[1])
    b = float(sys.argv[2])
except ValueError:
    print("Error: los dos parámetros tienen que ser números")
    sys.exit(1)

print(f"Sum: {a + b}")