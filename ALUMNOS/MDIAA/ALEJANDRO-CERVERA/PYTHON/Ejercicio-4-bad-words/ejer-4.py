
# EJERCICIO 4

# 1. FUNCIÓN DE NORMALIZACIÓN

def norm(s: str) -> str:
    return s.lower().strip()

# 2. CARGA DE PALABRAS PROHIBIDAS - proporcionado por el ejercicio

bad = set()                                  
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:                           
        w = line.strip()                     
        if w:                                
            bad.add(norm(w))                 

# 3. INPUT

palabra = input("Introduce una palabra: ")

# 4. VALIDACIÓN

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    if norm(palabra) in bad:                 
        print("NO CORRECTA")                
    else:
        print("CORRECTA")                   

# 5. COMPROBACIONES


