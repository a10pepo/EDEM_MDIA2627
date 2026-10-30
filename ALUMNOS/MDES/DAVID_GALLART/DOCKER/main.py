import sys

if len(sys.argv) > 3:
    print("Maximo se pueden sumar dos numeros")
else:
    n1 = float(sys.argv[1])
    n2 = float(sys.argv[2])


    print("Suma:", int(n1 + n2))