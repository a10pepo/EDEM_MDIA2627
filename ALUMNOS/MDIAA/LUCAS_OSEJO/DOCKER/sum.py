
import sys


def to_number(value):
    """Convierte el texto a int si se puede; si no, a float."""
    try:
        return int(value)
    except ValueError:
        return float(value)


if len(sys.argv) != 3:
    print("Uso: docker run pysum <num1> <num2>")
    sys.exit(1)

a = to_number(sys.argv[1])
b = to_number(sys.argv[2])
print(f"Sum: {a + b}")