#!/bin/bash

echo "El script debe ser reejecutable sin necesidad de modificarlo, por lo que debe borrar al inicio lo creado en la ejecución anterior"
rm -r PRUEBA

echo "1.Listar todos los archivos del directorio bin."
ls /bin

echo "2.Listar todos los archivos del directorio tmp."
ls /tmp

echo "3.Listar todos los archivos del directorio etc que empiecen por t"
ls /etc/t*

echo "4.Listar todos los archivos del directorio dev que empiecen por tty."
ls /dev/tty*

echo "5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3."
ls /dev/tty*3

echo "6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1."
ls /dev/t*C1

echo "7.Listar todos los archivos, incluidos los ocultos, del directorio raíz."
ls -a /

echo "8.Listar todos los archivos del directorio etc que no empiecen por t."
ls /etc/[!t]*

echo "9.Listar todos los archivos del directorio usr y sus subdirectorios."
ls -R /usr

echo "10.Cambiarse al directorio tmp, crear directorio PRUEBA."
cd /tmp
mkdir PRUEBA

echo "11.Verificar que el directorio actual ha cambiado."
pwd

echo "12.Mostrar el día y la hora actual."
date

echo "13.Con un solo comando posicionarse en el directorio $HOME."
cd $HOME

echo "14.Verificar que se está en él."
pwd

echo "15.Listar todos los ficheros del directorio HOME mostrando sus permisos."
ls -l $HOME

echo "16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA."
rm -r /tmp/PRUEBA/*

echo "17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312."
mkdir /tmp/PRUEBA/dir1
mkdir /tmp/PRUEBA/dir2
mkdir /tmp/PRUEBA/dir3
mkdir mkdir /tmp/PRUEBA/dir1/dir11
mkdir /tmp/PRUEBA/dir3/dir31
mkdir /tmp/PRUEBA/dir3/dir31/dir311
mkdir /tmp/PRUEBA/dir3/dir31/dir312

echo "18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA."
cp /etc/mtab /tmp/PRUEBA

echo "19.Copiar /etc/mtab en dir1, dir2 y dir3."
cp /etc/mtab /tmp/PRUEBA/dir1 
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3

echo "20.Comprobar el ejercicio anterior mediante un solo comando."
ls /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
