import sys

try:
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
    print(f"Sum: {num1 + num2}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)