# Entregable 1 - Linux

**1. Listar todos los archivos del directorio bin.**
```bash
ls /bin
```

**2. Listar todos los archivos del directorio tmp.**
```bash
ls /tmp
```

**3. Listar todos los archivos del directorio etc que empiecen por t**
```bash
ls /etc/t*
```

**4. Listar todos los archivos del directorio dev que empiecen por tty.**
```bash
ls /dev/tty*
```

**5. Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.**
```bash
ls /dev/tty*3 # estoy en otra carpeta, fuera de la raiz
```

**6. Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.**
```bash
ls /dev/t*C1 # ruta absoluta
```

**7. Listar todos los archivos, incluidos los ocultos, del directorio raíz.**
```bash
ls -a /
```

**8. Listar todos los archivos del directorio etc que no empiecen por t.**
```bash
ls /etc/[!t]*
```

**9. Listar todos los archivos del directorio usr y sus subdirectorios.**
```bash
# De esta forma listo tanto los archivos del directorio usr como los archivos de sus subdirectorios sin tener que entrar en cada uno haciendo un "ls" n veces.
find /usr -mindepth 1 -maxdepth 2

# Es otra alternativa, pero llegará a un nivel de profundidad total y recursivo en cada directorio y subdirectorio que entre, llegando a ser más de lo que se pide inicialmente.
ls -R /usr
```

**10. Cambiarse al directorio tmp, crear directorio PRUEBA.**
```bash
cd /tmp ; mkdir PRUEBA # Parto de la base que me cambie e ingresé a tmp por lo que no hay necesidad de dar la ruta absoluta para su creación
```

**11. Verificar que el directorio actual ha cambiado.**
```bash
ls # Asumo continuidad y que ya estoy en directorio tmp, con "ls" compruebo si se creó o no PRUEBA
```

**12. Mostrar el día y la hora actual.**
```bash
date
```

**13. Con un solo comando posicionarse en el directorio $HOME.**
```bash
cd $HOME
```

**14. Verificar que se está en él.**
```bash
pwd
```

**15. Listar todos los ficheros del directorio HOME mostrando sus permisos.**
```bash
ls -l $HOME # HOME es una ENV que tiene como valor /root por lo que es lo mismo que entrar al directorio /root y hacer un "ls -l"
```

**16. Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.**
```bash
rm -r /tmp/PRUEBA/*
```

**17. Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.**
```bash
mkdir /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
mkdir /tmp/PRUEBA/dir1/dir11 /tmp/PRUEBA/dir3/dir31
mkdir /tmp/PRUEBA/dir3/dir31/dir311 /tmp/PRUEBA/dir3/dir31/dir312
```

**18. Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.**
```bash
cp /etc/mtab /tmp/PRUEBA/
```

**19. Copiar /etc/mtab en dir1, dir2 y dir3.**
```bash
cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3
```

**20. Comprobar el ejercicio anterior mediante un solo comando.**
```bash
find /tmp/PRUEBA -mindepth 2 -maxdepth 2 -name mtab # Agregue el "mindepth" para que no arroje también la copia de "mtab" en PRUEBA y así solo se vean las copias del ejercicio 19.
```
