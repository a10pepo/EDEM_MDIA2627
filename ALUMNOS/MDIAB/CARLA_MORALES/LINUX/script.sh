#!/bin/bash

cd "$HOME"

echo "================================"
echo "INICIO DEL SCRIPT"
echo "================================"

echo "TAREA 1: Eliminar carpetas anteriores"
rm -rf Carpeta1 Carpeta2 Carpeta3

echo "TAREA 2: Crear las carpetas"
mkdir Carpeta1 Carpeta2 Carpeta3

echo "TAREA 3: Crear archivos"
touch Carpeta1/archivo1.txt
touch Carpeta1/archivo2.txt
touch Carpeta2/archivo3.txt
touch Carpeta2/archivo4.txt
touch Carpeta3/archivo5.txt

echo "TAREA 4: Mostrar el contenido"
ls -R

echo "================================"
echo "SCRIPT FINALIZADO"
echo "================================"
