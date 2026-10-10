# Ejercicio 1
# 1. Escribe el nombre de la calle de tu domicilio en una variable
# 2. Escribe el número de la calle en otra
# 3. Ciudad en una tercera
# 4. Código postal en la cuarta variable
# 5. Crea una quinta variable que concatene todas ellas
# 6. Imprime por pantalla la dirección
# 7. Crea una cadena (string) con una frase que contenga comillas internas e imprímela.
# 8. Luego muestra la longitud de esa cadena usando len(), imprímela con un mensaje del estilo "Esta cadena tiene x caracteres".

# calle:str = "Calle Aragón"
# numero_calle:str = "13"
# ciudad:str = "Valencia"
# codigo_postal:str = "46015"

# concatenar = f"{calle} {numero_calle} {ciudad} {codigo_postal}"
# frase = f'"X" vive en la {calle}, número {numero_calle}, en la ciudad de {ciudad}, con código postal {codigo_postal}.'

# print(concatenar)
# print(frase)
# print(len(f"Esta cadena tiene {frase} caracteres."))
# ---------------------------------------------------------------

# ¿Qué variables están mal escritas y por qué? Realiza primero tu hipótesis y luego ejecuta las variables para comprobarlo. 


# 1. mi_variable = "Economía"
# 2. otra_var = "Ejercicio
# 3. True = "Ejercicio"
# 4. mi variab1e = "Alpha"
# 5. import = 40
# 6. 81mi_variable = "Agua"
# 7. mi_variable10 = 6

# 1. Correcto.
# 2.Incorrecto, le falta " en el final .
# 3.Incorrecto, no podemos usar True como nombre de variable, ya que, pertenece al tipo de booleano.
# 4. Incorrecto, no se puede poner espacios entre el nombre de la variable.
# 5. Incorrecto, no podemos usar nombre de variable, este es una funcion para usar funciones de otros archivos
# 6. Incorrecto, no se pueden usar números delante en el nombre de la Variable
# 7. Correcto.
# ---------------------------------------------------------------
# * Crea dos variables numéricas: un `int` y un `float`
# * Comprueba sus tipos
# * Súmalas en otra nueva
# * ¿De qué tipo es la nueva variable?
# * Elimina las dos primeras variables creadas

# num1:int = 5
# num2:float = 20.1

# print(type(num1))
# print(type(num2))

# suma = num1 + num2

# print(type(suma))

# del num1, num2
# ---------------------------------------------------------------
# Practicaremos ahora los operadores que estuvimos viendo en clase. 

# Si te sirve, puedes investigar la lista de operadores [aquí](https://www.w3schools.com/python/python_operators.asp).

# 1. *Operadores aritméticos (suma, resta, multiplicación, división, módulo, potencia)* 
#     1) Crea dos variables a=10, b=3 y calcula:
#     - La suma a + b
#     - La resta a - b
#     - La multiplicación a * b
#     - La división a / b
#     - El módulo a % b

#     2) Calcula el resultado de (a + b) * 2 - 5
#     3) Usa división entera (//) para calcular cuántas veces cabe b en a
#     4) Encuentra la raíz cuadrada de a usando potencia: a ** 0.5
#     5) La potencia a ** b

# a:int = 10
# b:int = 3

# print(a + b)
# print(a - b)
# print(a * b)
# print(a / b)
# print(a % b)

# print(a // b)
# print(a ** 0.5)
# print(a ** b)

# *Operadores de Comparación (==, !=, >, <, >=, <=)*
#     1) Compara si a es igual a b
#     2) Comprueba si a es distinto de b
#     3) Determina si a es mayor que b
#     4) Verifica si b es menor o igual que a
#     5) Comprueba si a + 5 es mayor o igual que b * 2

# print (a == b)
# print(a != b)
# print(a > b)
# print(b <= a)
# print(a + 5 >= b * 2)

# *Operadores Lógicos (and, or, not)*
#     1) Comprueba si a > 5 y b < 5
#     2) Comprueba si a < 5 o b < 5
#     3) Aplica not a la expresión (a == b)
#     4) Comprueba si a es mayor que 5 y no es igual a 10

# print(a > 5 and b < 5)
# print(a < 5 or b > 5)
# print(not a == b)
# print(a > 5 and a != 10)

# Ahora tenemos las siguientes variables:

A = 4
B = "Text"
C = 4.1

# Comprueba:
# 1. Si A y B son equivalentes
# 2. Si A y C NO son equivalentes
# 3. Si A es mayor que C 
# 4. Si C es menor o igual que A
# 5. Si B NO es equivalente a C

# print(A == B)
# print(A != C)
# print(A > C)
# print(C <= A)
# print(B != C)

# *Operadores de Pertenencia (in, not in)*
#     1) Declara una lista lista = y verifica si 3 está en la lista
#     2) Comprueba si 6 no está en la lista
#     3) Declara un string texto = "python" y verifica si "y" está en texto
#     4) Comprueba si "z" no está en texto



# *Operadores de Asignación (=, +=, -=, *=, /=, %=, **=, //=)*
#     1) Crea una variable x = 10. Súmale 5 usando asignación abreviada x += 5
#     2) Resta 3 a x usando x -= 3
#     3) Multiplica x por 2 con x *= 2
#     4) Divide x entre 4 usando x /= 4
#     5) Obtén el módulo de x entre 3 con x %= 3
#     6) Eleva x a la potencia 3 usando x **= 3
#     7) Realiza una división entera de x entre 2 con x //= 2