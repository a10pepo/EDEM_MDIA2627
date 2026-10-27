#!/bin/bash
cd ~

rm -rf carpeta1
echo "Borrando carpeta1 si existese"

rm -rf carpeta2
echo "Borrando carpeta2 si existese"

mkdir carpeta1
echo "Carpeta1 creada correctamente!"

mkdir carpeta1/carpeta11
echo "Subcarpeta11 creada correctamente!"

mkdir carpeta2
echo "Carpeta2 creada correctamente!"

mkdir carpeta2/carpeta21
echo "Subcarpeta21 creada correctamente!"

echo "Todas las carpetas y subcarpetas creadas correctamente!"