from sys import argv


def suma(a:int, b:int):
    return a + b

res = suma(int(argv[1]), int(argv[2]))

print(f"Sum: {res}")