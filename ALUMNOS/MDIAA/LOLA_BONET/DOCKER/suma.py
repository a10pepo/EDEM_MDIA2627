import sys

def suma():
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        print(f"Sum: {a + b}")
    except (ValueError, IndexError):
        print("No son dos números")
        
suma()