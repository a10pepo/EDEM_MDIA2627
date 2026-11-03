import argparse


def suma_dos (a, b):
    """
    Función para sumar dos números pasados como parametros por la consola.

    Returns:
        int or float: La suma de a y b.
    """
    return a + b


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    args = parser.parse_args()

    print(f"Sum: {suma_dos(args.a, args.b):g}")

