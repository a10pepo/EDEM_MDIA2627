#!/bin/bash

CARPETA="$(cd "$(dirname "$0")" && pwd)"
PRUEBA="$CARPETA/PRUEBA"

rm -rf "$PRUEBA"
cd "$CARPETA" || exit 1

echo "1. Listar los archivos de /bin"
ls /bin

echo "2. Listar los archivos de /tmp"
ls /tmp

echo "3. Listar los archivos de /etc que empiezan por t"
ls -d /etc/t*

echo "4. Listar los archivos de /dev que empiezan por tty"
ls -d /dev/tty*

echo "5. Listar los archivos de /dev que empiezan por tty y acaban en 3"
ls -d /dev/tty*3

echo "6. Listar los archivos de /dev que empiezan por t y acaban en C1"
ls -d /dev/t*C1

echo "7. Listar los archivos, incluidos los ocultos, del directorio raíz"
ls -a /

echo "8. Listar los archivos de /etc que no empiezan por t"
ls -d /etc/[!t]*

echo "9. Listar los archivos de /usr y sus subdirectorios"
ls -R /usr

echo "10. Crear la carpeta PRUEBA dentro de LINUX"
mkdir -p "$PRUEBA"

echo "11. Mostrar la carpeta de trabajo"
pwd

echo "12. Mostrar el día y la hora"
date

echo "13. Ir a la carpeta HOME"
cd "$HOME"

echo "14. Comprobar la carpeta actual"
pwd

echo "15. Listar los archivos de HOME con sus permisos"
ls -la "$HOME"

echo "16. Borrar el contenido visible de PRUEBA"
rm -rf "$PRUEBA"/*

echo "17. Crear las carpetas solicitadas dentro de PRUEBA"
mkdir -p "$PRUEBA/dir1/dir11" "$PRUEBA/dir2" "$PRUEBA/dir3/dir31/dir311" "$PRUEBA/dir3/dir31/dir312"

echo "18. Copiar /etc/mtab en PRUEBA"
cp /etc/mtab "$PRUEBA/"

echo "19. Copiar /etc/mtab en dir1, dir2 y dir3"
cp /etc/mtab "$PRUEBA/dir1/"
cp /etc/mtab "$PRUEBA/dir2/"
cp /etc/mtab "$PRUEBA/dir3/"

echo "20. Comprobar las copias"
ls -l "$PRUEBA/dir1/mtab" "$PRUEBA/dir2/mtab" "$PRUEBA/dir3/mtab"
