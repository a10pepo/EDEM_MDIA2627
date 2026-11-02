1.Listar todos los archivos del directorio bin.
    ls /bin

2.Listar todos los archivos del directorio tmp.
    ls /tmp

3.Listar todos los archivos del directorio etc que empiecen por t
    ls /etc/t*

4.Listar todos los archivos del directorio dev que empiecen por tty.
    ls /dev/tty*

5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.
    ls /dev/tty*3
    Si tienen extensión (ej: .txt) hay que poner un *, que sino no los encuentra

6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.
    ls /dev/t*C1

7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
    ls -a /

8.Listar todos los archivos del directorio etc que no empiecen por t.
    ls /etc/[!t]* 

9.Listar todos los archivos del directorio usr y sus subdirectorios.
    find /usr 
    Si hay que limitar la profundidad uso -maxdepth x

10.Cambiarse al directorio tmp, crear directorio PRUEBA.
    cd /tmp
    mkdir PRUEBA

11.Verificar que el directorio actual ha cambiado.
    pwd

12.Mostrar el día y la hora actual.
    date

13.Con un solo comando posicionarse en el directorio $HOME.
    cd $HOME

14.Verificar que se está en él.
    pwd

15.Listar todos los ficheros del directorio HOME mostrando sus permisos.
    ls -l $HOME

16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.
    rm -r /home/pepe/PRUEBA/*

17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.
    mkdir /home/pepe/PRUEBA/dir1 /home/pepe/PRUEBA/dir2 /home/pepe/PRUEBA/dir3
    mkdir /home/pepe/PRUEBA/dir1/dir11 
    mkdir /home/pepe/PRUEBA/dir3/dir31
    mkdir /home/pepe/PRUEBA/dir3/dir31/dir311 /home/pepe/PRUEBA/dir3/dir31/dir312

18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.
    cp /etc/mtab /home/pepe/PRUEBA

19.Copiar /etc/mtab en dir1, dir2 y dir3.
    cp /etc/mtab /home/pepe/PRUEBA/dir1
    cp /etc/mtab /home/pepe/PRUEBA/dir2
    cp /etc/mtab /home/pepe/PRUEBA/dir3

20.Comprobar el ejercicio anterior mediante un solo comando.
    find /home/pepe/PRUEBA/*/mtab
