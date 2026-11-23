# Linux_Comandos

Para entregar este ejercicio, debes copiar este archivo en tu carpeta de alumno y completar las respuestas a las preguntas que se formulan en el mismo.
Una vez completado, debes subirlo a vuestro repositorio remoto de GitHub y realizar una Pull Request poniendo a Pedro Nieto como reviewer.


Ejercicio de comandos en la consola de linux.

1.Listar todos los archivos del directorio bin.

Se podría hacer ls /bin/ o entrar primero en bin haciendo cd bin y posteriormente ls para ver los archivos

2.Listar todos los archivos del directorio tmp.

ls /tmp/

3.Listar todos los archivos del directorio etc que empiecen por t 

Primero cd etc y luego ls t*
  
4.Listar todos los archivos del directorio dev que empiecen por tty.

Primero cd etc y luego ls tty*

5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.

ls /dev/tty*3

6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.

ls /dev/t*C1

7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
C
uando estas en el directorio raiz / usas ls -a

8.Listar todos los archivos del directorio etc que no empiecen por t.

ls /etc/[!t]*

9.Listar todos los archivos del directorio usr y sus subdirectorios.

ls /usr -R

10.Cambiarse al directorio tmp, crear directorio PRUEBA.

cd tmp y despues usar mkdir PRUEBA

11.Verificar que el directorio actual ha cambiado.

Estando dentro del directorio tmp usamos ls. Si no ls /tmp/

12.Mostrar el día y la hora actual.

date

13.Con un solo comando posicionarse en el directorio $HOME.

cd $HOME o cd ~
 
14.Verificar que se está en él.

pwd

15.Listar todos los ficheros del directorio HOME mostrando sus permisos.

Estando en en ese directorio usar ls -l

16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.

cd tmp y depues cd PRUEBA y por ultimo rm -r

17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.

mkdir /tmp/PRUEBA/dir1 -- mkdir /tmp/PRUEBA/dir2 -- mkdir /tmp/PRUEBA/dir3 -- mkdir /tmp/PRUEBA/dir1/dir11 -- mkdir /tmp/PRUEBA/dir3/dir31 
cd /tmp/PREUBA/dir3/dir31 y mkdir dir311 dir312

18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.

cp /etc/mtab /tmp/PRUEBA

19.Copiar /etc/mtab en dir1, dir2 y dir3.

cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3

20.Comprobar el ejercicio anterior mediante un solo comando.

find /tmp/PRUEBA -name 'mtab'