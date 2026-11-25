import sys

if len(sys.argv) != 3:
    print("Error: debes indicar dos números.")
    sys.exit(1)

try:
    number1 = float(sys.argv[1])
    number2 = float(sys.argv[2])
except ValueError:
    print("Error: los dos argumentos deben ser números.")
    sys.exit(1)

print(f"Sum: {number1 + number2:g}")
