#Ejercicio 1
nombre = "Marina de Empresas 2025"
print(len(nombre))
print(nombre[0])


#Ejercicio 2
festivo = True
if (festivo == True): 
    print("Hoy es fiesta voy a echarme una siesta!!")
else: 
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


#Ejercicio 4
def ultimoCaracter(cadena): 
    if (type(cadena) != str):
        return "Debo ser ejecutada con un string"
    else: 
        return cadena[-1]


#Ejercicio 5
def norm(s):
    s = s.lower()
    s = s.strip()
    return s


palabra = input()

if (palabra == "" or " " in palabra):
    print("Introduce una sola palabra (sin espacios).")

else:
    bad = set()

    with open("bad_words.txt", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                bad.add(norm(w))

    palabra = norm(palabra)

    if (palabra in bad):
        print("NO CORRECTA")
    else:
        print("CORRECTA")