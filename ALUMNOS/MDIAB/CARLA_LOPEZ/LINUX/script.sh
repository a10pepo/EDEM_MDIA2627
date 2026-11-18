#!/bin/bash

cd "$(dirname "$0")" || exit 1

echo "Iniciando el script"

echo "1) eliminar los resultados de la ejecución anterior"
rm -rf PRUEBA
#r para eliminar la carpeta y todo su contenido
#f para que no de error si la carpeta no existe

echo "2) crear la carpeta PRUEBA"
mkdir PRUEBA

echo "3) Crear las carpetas dir1, dir2 y dir3"
cd PRUEBA
mkdir dir1 
mkdir dir2 
mkdir dir3

echo "4) Crear las subcarpetas"
cd dir1
mkdir dir11
echo "Creada dir11"

cd ..
cd dir3
mkdir dir31
echo "Creada dir31"

cd dir31
mkdir dir311
mkdir dir312
echo "Creadas dir311 y dir312"

echo "5) Copiar el archivo mtab en PRUEBA"
cd ..
cd ..

cp /etc/mtab .
echo "Archivo copiado en PRUEBA"

echo "6) Copiar el archivo mtab en dir1, dir2 y dir3"
cp /etc/mtab dir1
echo "Archivo copiado en dir1"

cp /etc/mtab dir2
echo "Archivo copiado en dir2"

cp /etc/mtab dir3
echo "Archivo copiado en dir3"

echo "7) Comprobar que se ha copiado el archivo en dir1, dir2 y dir3"
ls dir*/mtab



