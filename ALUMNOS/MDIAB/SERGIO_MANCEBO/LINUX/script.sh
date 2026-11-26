
#!/bin/bash

# LIMPIEZA INICIAL
echo "Limpiando la ejecucion anterior..."
rm -rf /tmp/PRUEBA

# 1. Listar todos los archivos del directorio bin
echo "TAREA 1: Listando directorio bin..."
ls /bin

# 2. Listar todos los archivos del directorio tmp
echo "TAREA 2: Listando directorio tmp..."
ls /tmp

# 3. Listar archivos de etc que empiezan por t
echo "TAREA 3: Archivos de etc que empiezan por t..."
ls /etc/t*

# 4. Listar archivos de dev que empiezan por tty
echo "TAREA 4: Archivos de dev que empiezan por tty..."
ls /dev/tty*

# 5. Listar archivos de dev que empiezan por tty y acaban en 3
echo "TAREA 5: Archivos de dev que empiezan por tty y acaban en 3..."
ls /dev/tty*3

# 6. Listar archivos de dev que empiezan por t y acaban en C1
echo "TAREA 6: Archivos de dev que empiezan por t y acaban en C1..."
ls /dev/t*C1

# 7. Listar todos los archivos, incluidos los ocultos, del directorio raiz
echo "TAREA 7: Listando directorio raiz, incluidos los ocultos..."
ls -a /

# 8. Listar archivos de etc que no empiezan por t
echo "TAREA 8: Archivos de etc que no empiezan por t..."
ls /etc/[!t]*

# 9. Listar archivos de usr y sus subdirectorios
echo "TAREA 9: Listando directorio usr de forma recursiva..."
ls -R /usr

# 10. Cambiar a tmp y crear PRUEBA
echo "TAREA 10: Creando directorio PRUEBA..."
cd /tmp
mkdir PRUEBA

# 11. Verificar el directorio actual
echo "TAREA 11: Comprobando directorio actual..."
pwd

# 12. Mostrar fecha y hora
echo "TAREA 12: Mostrando fecha y hora..."
date

# 13. Acceder al directorio HOME
echo "TAREA 13: Accediendo al directorio HOME..."
cd ~

# 14. Verificar que estamos en HOME
echo "TAREA 14: Comprobando directorio HOME..."
pwd

# 15. Listar archivos de HOME mostrando permisos
echo "TAREA 15: Listando archivos de HOME y sus permisos..."
ls -la /home

# 16. Borrar archivos y directorios visibles de PRUEBA
echo "TAREA 16: Eliminando contenido visible de PRUEBA..."
rm -rf /tmp/PRUEBA/*

# 17. Crear estructura de directorios
echo "TAREA 17: Creando estructura de directorios..."
mkdir -p /tmp/PRUEBA/{dir1/dir11,dir2,dir3/dir31/{dir311,dir312}}

# 18. Copiar mtab a PRUEBA
echo "TAREA 18: Copiando mtab a PRUEBA..."
cp -r /etc/mtab /tmp/PRUEBA/

# 19. Copiar mtab a dir1, dir2 y dir3
echo "TAREA 19: Copiando mtab a los tres directorios..."
cp -r /etc/mtab /tmp/PRUEBA/dir1/
cp -r /etc/mtab /tmp/PRUEBA/dir2/
cp -r /etc/mtab /tmp/PRUEBA/dir3/

# 20. Comprobar el resultado
echo "TAREA 20: Comprobando estructura final..."
ls -R /tmp/PRUEBA

echo "EJERCICIO FINALIZADO"
