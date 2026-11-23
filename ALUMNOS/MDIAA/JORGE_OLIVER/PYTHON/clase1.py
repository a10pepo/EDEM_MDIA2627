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

# A = 4
# B = "Text"
# C = 4.1

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

# lista = [3, 7, 10]
# texto:str = "Python"
# print(3 in lista)
# print(6 in lista)
# print("y" in texto)
# print("z" not in texto)

# *Operadores de Asignación (=, +=, -=, *=, /=, %=, **=, //=)*
#     1) Crea una variable x = 10. Súmale 5 usando asignación abreviada x += 5
#     2) Resta 3 a x usando x -= 3
#     3) Multiplica x por 2 con x *= 2
#     4) Divide x entre 4 usando x /= 4
#     5) Obtén el módulo de x entre 3 con x %= 3
#     6) Eleva x a la potencia 3 usando x **= 3
#     7) Realiza una división entera de x entre 2 con x //= 2

# x = 10
# x += 5
# print(x)
# x -= 3
# print(x)
# x *= 2
# print(x)
# x /=4
# print(x)
# x %= 3
# print(x)
# x ** 3
# print(x)
# x //= 2
# print(x)
# ---------------------------------------------------------------
# #### Ejercicio 5
# Utilizaremos como base el siguiente string:

#     "A quien madruga, dios le ayuda"

# Imprime por pantalla lo siguiente:
# 1. Pasarlo todo a mayúsculas
# 2. Pasarlo todo a minúsculas
# 3. Pasar a mayúsculas solo las iniciales de las palabras
# 4. Crea una lista dividiendo por sus espacios en diferentes string
# 5. Sustituye las comas `,` por puntos y comas `;`
# 6. Elimina las `a` minúsculas

# frase:str = "A quien madruga, dios le ayuda"

# print(frase.upper())
# print(frase.lower())
# print(frase.title())
# print(frase.split())
# print(frase.replace(",", ";"))
#  ---------------------------------------------------------------
# #### Ejercicio 6
# En este ejercicio se va a crear una lista con distintos elementos. 

# Crea primero las variables que luego añadiremos a la lista. Sigue las instrucciones detalladas a continuación:

# 1. Crea una variable llamada `puntuación` de tipo Integer que represente la puntuación obtenida en un juego.
# 2. Crea una variable llamada `nombre_equipo` de tipo String que contenga el nombre de tu equipo favorito de deportes seguido de un espacio en blanco y el deporte que practicas.
# 3. Crea una variable llamada `promedio_tiempo` con el promedio de tiempo en horas que dedicas diariamente al estudio o trabajo, de tipo float.
# 4. Crea una variable llamada `es_habil` de tipo Boolean True si eres diestro y False si eres zurdo.
# 5. Crea una variable llamada `lista_compras` de tipo List que contenga los nombres de los cinco alimentos que más consumes. Cada elemento debe ser de tipo String.
# 6. Crea una variable llamada `tupla_mascotas` de tipo Tuple que incluya el nombre, la edad y la especie de tus dos mascotas -en dos tuplas, una por mascota-.
# 7. Crea una variable llamada `dict_contactos` con tres keys y tres values. Una key es `amigos`, con los nombres y apellidos ("Juan Pablo Pérez García") de tus dos amigos como value. Otra key es `telefonos`, con sus números de teléfono como value. La última key es `emails`, con sus direcciones de correo electrónico como value.
# 8. Añade todos estos elementos en una lista llamada `lista_actividades` en el orden de aparición **usando la función de lista que aprendimos en clase**.
# 9. Responde en un comentario a la siguiente pregunta: ¿Cómo podrías verificar si un elemento está presente en `lista_actividades` antes de agregarlo a la lista para evitar duplicados?

puntuacion:int = 0

nombre_equipo:str = "Valencia Futbol"

promedio_tiempo: float = 20.5

es_habil:bool = True

lista_compras:list = ["huevo", "aguacate", "pollo", "brocoli", "pimiento" ]

tupla_mascotas1:tuple = ("Eren", 6, "perro")

tupla_mascotas2:tuple = ("Pepin", 1, "gato")

dict_contactos: dict = {
    "amigos": ["Pepe Luis González", "Angel Perez Garcia", "Jose Manuel Linares"],
    "telefonos": ["687697788", "678997643", "634356823"],
    "emails": ["pepe@gmail.com", "angel@gmail.com", "jose@gmail.com"]
}

lista_actividades: list = [puntuacion, nombre_equipo, promedio_tiempo, es_habil, lista_compras, tupla_mascotas1, tupla_mascotas2, dict_contactos]
 
# 9. Responde en un comentario a la siguiente pregunta: ¿Cómo podrías verificar si un elemento está presente en `lista_actividades` antes de agregarlo a la lista para evitar duplicados?

# ejemplo:
# if puntuacion in lista_actividades:
#     print("Duplicado")
# else:
#     print("No duplicado")

#  ---------------------------------------------------------------
#### Ejercicio 6

# En este ejercicio seguimos trabajando con diccionarios. 

# 1. Crea un diccionario llamado agenda con tres entradas iniciales, por ejemplo:
#     - "Ana" → "654123987"
#     - "Luis" → "678555111"
#     -"Marta" → "622444333"

# 2. Realiza las siguientes operaciones usando métodos de diccionario (puedes investigar en [esta página](https://www.w3schools.com/python/python_dictionaries_methods.asp) los distintos métodos built-in):
#     1) Muestra todas las claves (nombres) y todos los valores (números).
#     2) Usa algún método para obtener el número de "Luis". ¿Qué ocurre si buscas el número de "Pedro", que no existe?
#     3) Añade un nuevo contacto llamado "Pedro" con su número.
#     4) Muestra todos los pares nombre-teléfono.
#     5) Borra a "Marta" de la agenda e imprime la agenda resultante. ***IMPORTANTE!*** Utiliza el método que te permita guardar a "Marta" en una lista de "Eliminados"
#     6) Finalmente, limpia toda la agenda y confirma que está vacía.

# agenda: dict = {
#     "Ana" : "654123987",
#     "Luis" : "678555111",
#     "Marta" : "622444333"
# }
# print(agenda)
# print(agenda.get("Pedro"))
# agenda.update({"Pedro":"657348374"})
# eliminados = agenda.pop("Marta")
# print(agenda)
# print(eliminados)
# agenda.clear()
# print(agenda)

# #  ---------------------------------------------------------------
# #### Ejercicio 7

# Ahora vamos a practicar los métodos con listas. Si quieres investigar un poco, te recomendamos [esta página](https://www.w3schools.com/python/python_lists_methods.asp)

# Crea una lista llamada "peliculas" con los títulos de tus pelis preferidas, por ejemplo:

peliculas: list = ["Gladiator", "Seven", "Shrek", "1917"]

# Realiza estas operaciones usando métodos de listas:

# a) Imprime todas las películas.

# print("Mis peliculas favoritas son:", peliculas)

# b) Añade "El Padrino" al final.

# peliculas.append("El Padrino")
# print("Mis peliculas favoritas son:", peliculas)

# # c) Inserta "Memento" en la posición 2.

# peliculas.insert(1, "Memento")
# print("Mis peliculas favoritas son:", peliculas)

# # d) Elimina "Gladiator".

# peliculas.remove("Gladiator")
# print("Mis peliculas favoritas son:", peliculas)

# e) Elimina y muestra la última película. Investiga si puedes hacer lo mismo con cualquier elemento de la lista, o sólo con el último. Contéstalo en un comentario.

# del peliculas [-1]
# print("Mis peliculas favoritas son:", peliculas)
#afirmativo, en el caso de querer eliminar otro valor, tendria que indicar la posicion en la que se encuentra el valor

# f) Ordena la lista alfabéticamente.

# peliculas.sort()
# print("Mis peliculas favoritas en orden alfabético:", peliculas)

# g) Vacía la lista y muestra que está vacía.

# peliculas.clear()
# print("Mis peliculas favoritas son:", peliculas)

# #  ---------------------------------------------------------------
# #### Ejercicio 8

# Practicaremos ahora los Condicionales que hemos visto en clase. Ya adivinarás, te recomendamos investigar un poquito para terminar de fijar [aquí](https://www.w3schools.com/python/python_conditions.asp)

# Evalúa las notas de examen de la clase. 
# 1. Crea una variable nota con un valor numérico entre 0 y 100 que represente la calificación de un examen.

nota:int = 100
    
# 2. Usa sentencias `if` y `else` anidadas para imprimir la siguiente evaluación según la nota:
#     - Si la nota es mayor o igual a 90, imprime: *"Excelente"*
if nota > 100:
    print("Nota inválida")
elif nota >= 90:
    print("Excelente", nota)
elif nota >= 70:
    print("Bueno", nota)
elif nota >= 50:
    print("Suficiente", nota)
elif nota >= 0:
    print("Insuficiente,", nota)
elif nota < 0:
    print("Nota inválida")
    
#     - Si la nota está entre 70 y 89 (inclusive), imprime: *"Bueno"*
#     - Si la nota está entre 50 y 69 (inclusive), imprime: *"Suficiente"*
#     - Si la nota es menor que 50, imprime: *"Insuficiente"*

# #  ---------------------------------------------------------------
# #### Ejercicio 9

# **Para cerrar: Importancia de documentar el código:**

# Documentar tu código usando comentarios es *esencial* para que tú y otros programadores puedan entender fácilmente lo que hace cada parte del código, especialmente cuando el proyecto crece o pasa tiempo sin tocarlo. Los comentarios permiten explicar la lógica, el propósito de variables, funciones y bloques de código, y apuntar detalles relevantes que no se ven directamente en el código.

# Además, comentar el código ayuda a detectar errores y facilita el trabajo en equipo, ya que otros pueden seguir el flujo sin confusión. También es útil para que los profesores puedan evaluar el proceso de razonamiento detrás de las soluciones.

# Por eso, como último ejercicio en esta práctica, documenta todo el código que hayan escrito hasta ahora, agregando comentarios claros que expliquen qué hace cada sección y por qué.

# [Aquí](https://peps.python.org/pep-0008/#comments) tienes un recurso si quieres investigar un poco sobre comentarios en Python.