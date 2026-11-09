
# 1. Listar todos los archivos del directorio bin
ls /bin

# 2. Listar todos los archivos del directorio tmp
ls /tmp

# 3. Listar archivos de etc que empiecen por t
ls /etc/t*

# 4. Listar archivos de dev que empiecen por tty
ls /dev/tty*

# 5. Listar archivos de dev que empiecen por tty y acaben en 3
ls /dev/tty*3

# 6. Listar archivos de dev que empiecen por t y acaben en C1
ls /dev/t*C1

# 7. Listar todos los archivos, incluidos ocultos, del directorio raíz
ls -a /

# 8. Listar archivos de etc que no empiecen por t
ls /etc/[^t]*

# 9. Listar todos los archivos del directorio usr y sus subdirectorios
ls -R /usr

# 10. Cambiarse a tmp y crear directorio PRUEBA
cd /tmp
mkdir PRUEBA

# 11. Verificar que el directorio actual ha cambiado
pwd

# 12. Mostrar día y hora actual
date

# 13. Posicionarse en HOME con un solo comando
cd $HOME

# 14. Verificar que se está en HOME
pwd

# 15. Listar ficheros de HOME mostrando sus permisos
ls -l $HOME

# 16. Borrar archivos y directorios visibles de PRUEBA
rm -r /tmp/PRUEBA/*

# 17. Crear estructura de directorios
mkdir -p /tmp/PRUEBA/dir1/dir11
mkdir -p /tmp/PRUEBA/dir2
mkdir -p /tmp/PRUEBA/dir3/dir31/dir311
mkdir -p /tmp/PRUEBA/dir3/dir31/dir312

# 18. Copiar /etc/mtab a PRUEBA
cp /etc/mtab /tmp/PRUEBA

# 19. Copiar /etc/mtab a dir1, dir2 y dir3
cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3

# 20. Comprobar el ejercicio anterior con un solo comando
ls -l /tmp/PRUEBA/dir{1,2,3}/mtab
