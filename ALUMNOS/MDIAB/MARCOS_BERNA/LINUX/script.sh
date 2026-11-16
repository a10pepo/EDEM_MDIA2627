#!/bin/bash

# =====================================================
#  Script que automatiza el ejercicio Linux_Comandos
#  Autor: Marcos Berna
# =====================================================

# Directorio de trabajo: carpeta LINUX dentro de la carpeta del usuario
WORKDIR="$HOME/LINUX"
PRUEBA="$WORKDIR/PRUEBA"

echo "=== Preparación: borrando lo creado en la ejecución anterior ==="
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

echo "=== Tarea 1: Listar todos los archivos del directorio bin ==="
ls /bin

echo "=== Tarea 2: Listar todos los archivos del directorio tmp ==="
ls /tmp

echo "=== Tarea 3: Listar los archivos de etc que empiezan por t ==="
ls -d /etc/t*

echo "=== Tarea 4: Listar los archivos de dev que empiezan por tty ==="
ls -d /dev/tty* 2>/dev/null || echo "No hay archivos que cumplan la condición"

echo "=== Tarea 5: Listar los archivos de dev que empiezan por tty y acaban en 3 ==="
ls -d /dev/tty*3 2>/dev/null || echo "No hay archivos que cumplan la condición"

echo "=== Tarea 6: Listar los archivos de dev que empiezan por t y acaban en C1 ==="
ls -d /dev/t*C1 2>/dev/null || echo "No hay archivos que cumplan la condición"

echo "=== Tarea 7: Listar todos los archivos, incluidos los ocultos, del directorio raíz ==="
ls -a /

echo "=== Tarea 8: Listar los archivos de etc que no empiezan por t ==="
ls -d /etc/[!t]*

echo "=== Tarea 9: Listar todos los archivos de usr y sus subdirectorios ==="
ls -R /usr

echo "=== Tarea 10: Cambiarse al directorio de trabajo y crear el directorio PRUEBA ==="
cd "$WORKDIR"
mkdir PRUEBA

echo "=== Tarea 11: Verificar que el directorio actual ha cambiado ==="
pwd

echo "=== Tarea 12: Mostrar el día y la hora actual ==="
date

echo "=== Tarea 13: Posicionarse en el directorio HOME ==="
cd

echo "=== Tarea 14: Verificar que se está en HOME ==="
pwd

echo "=== Tarea 15: Listar los ficheros de HOME mostrando sus permisos ==="
ls -la ~

echo "=== Tarea 16: Borrar todos los archivos y directorios visibles de PRUEBA ==="
rm -rf "$PRUEBA"/*

echo "=== Tarea 17: Crear la estructura de directorios dentro de PRUEBA ==="
cd "$PRUEBA"
mkdir dir1 dir2 dir3
cd dir1
mkdir dir11
cd ../dir3
mkdir dir31
cd dir31
mkdir dir311 dir312

echo "=== Tarea 18: Copiar /etc/mtab a PRUEBA ==="
cp /etc/mtab "$PRUEBA"/

echo "=== Tarea 19: Copiar /etc/mtab en dir1, dir2 y dir3 ==="
cp /etc/mtab "$PRUEBA"/dir1/
cp /etc/mtab "$PRUEBA"/dir2/
cp /etc/mtab "$PRUEBA"/dir3/

echo "=== Tarea 20: Comprobar el resultado con un solo comando ==="
ls -R "$PRUEBA"

echo "=== Script terminado ==="