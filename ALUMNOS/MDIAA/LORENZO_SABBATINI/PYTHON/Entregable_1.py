#Ejercicio 1
nombre = "Marina de Empresas 2025"
print(len(nombre))
print(nombre[0])

#Ejercicio 2
festivo: bool = False

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#Ejercicio 4
def ultimoCaracter(x):
    if type(x) == str:
        return(x[-1])
    else:
        return("Debo ser ejecutada con un string")

print(ultimoCaracter("Ciao"))
print(ultimoCaracter(44))

#Ejercicio 5
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

y = input("Escribe una palabra: ")

def norm(s: str) -> str:
    return s.strip().lower()
    
    '''
    s.strip() = elimina espacios y tabs
    .lower() = convierte todos en letras minuscolas
    '''


print(y)