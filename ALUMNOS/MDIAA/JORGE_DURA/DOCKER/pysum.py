import sys


def suma(a, b):
    return a + b


def to_number(valor):
    # Acepta enteros ("3") y decimales ("3.5")
    try:
        return int(valor)
    except ValueError:
        return float(valor)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: docker run pysum <num1> <num2>")
        sys.exit(1)

    try:
        a = to_number(sys.argv[1])
        b = to_number(sys.argv[2])
    except ValueError:
        print("Error: los dos parámetros deben ser números")
        sys.exit(1)

    print(f"Sum: {suma(a, b)}")
