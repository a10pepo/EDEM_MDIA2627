import argparse
from decimal import Decimal, InvalidOperation


def parse_numero(valor):
    try:
        return Decimal(valor)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("Introduce un número válido") from error


def main():
    parser = argparse.ArgumentParser(description="Suma dos números")
    parser.add_argument("numero1", type=parse_numero)
    parser.add_argument("numero2", type=parse_numero)
    args = parser.parse_args()

    print(f"Sum: {args.numero1 + args.numero2}")


if __name__ == "__main__":
    main()