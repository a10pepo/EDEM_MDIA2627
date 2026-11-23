def norm(s:str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

s = input("Introduce una sola palabra (sin espacios).: ")
while s == "" or " "in s:
    s = input("Introduce una sola palabra (sin espacios).: ")
   
s_norm = norm(s)

if s_norm in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")



