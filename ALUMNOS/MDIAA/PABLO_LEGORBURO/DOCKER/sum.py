import sys


def main():
    # Comprobar que se pasan exactamente dos números
    if len(sys.argv) != 3:
        print("Uso: docker run pysum <numero1> <numero2>")
        sys.exit(1)

    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
    except ValueError:
        print("Error: los dos parámetros deben ser números")
        sys.exit(1)

    resultado = num1 + num2

    # Si el resultado es entero (ej. 7.0), mostrarlo como 7
    if resultado.is_integer():
        resultado = int(resultado)

    print(f"Sum: {resultado}")


if __name__ == "__main__":
    main()