<p align="right">10/11/2026</p>

# Entregable: Comandos de Linux

**Sergio Mancebo Campos** 

## Ejercicio de comandos en la consola de linux.

  ### 1.Listar todos los archivos del directorio bin.
  ```bash
  ls /bin
  ```
  ---

  ### 2.Listar todos los archivos del directorio tmp.
  ```bash
  ls /tmp
  ```
  ---
    
  ### 3.Listar todos los archivos del directorio etc que empiecen por t 
  ```bash
  ls /etc/t*
  ```
  ---

  ### 4.Listar todos los archivos del directorio dev que empiecen por tty.
  ```bash
  ls /dev/tty*
  ```
  ---  
    
  ### 5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.
  ```bash
  ls /dev/tty*3
  ```
  ---
    
  ### 6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.
  ```bash
  ls /dev/t*C1
  ```
  ---  

  ### 7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
  ```bash
  ls -a /
  ```
  >El parámetro `-a`: incluye los archivos y directorios ocultos.
  
  ---
       
  ### 8.Listar todos los archivos del directorio etc que no empiecen por t.
  ```bash
  ls /etc/[!t]*
  ```
  --- 

  ### 9.Listar todos los archivos del directorio usr y sus subdirectorios.
  ```bash
  ls -R /usr
  ```
  >El parámetro `-R` representa la opción recursiva, que indica al comando `ls` que no se limite a mostrar los elementos que están en el nivel principal de `/usr`, sino que descienda y entre en cada subdirectorio, y dentro de los subdirectorios de esos subdirectorios, listando progresivamente todo el contenido del árbol de carpetas.

  **Alternativa:** `find /usr`

  >El comando `find` permite buscar dentro de una ruta especificada. En este caso, busca y muestra todos los archivos y directorios que se encuentran dentro de /usr y sus subdirectorios.
  --- 

  ### 10.Cambiarse al directorio tmp, crear directorio PRUEBA.
  ```bash
  cd /tmp
  mkdir PRUEBA
  ```
 ---

  ### 11.Verificar que el directorio actual ha cambiado.
  ```bash
  pwd
  ```
  --- 

  ### 12.Mostrar el día y la hora actual.
  ```bash
  date
  ```
  ---  

  ### 13.Con un solo comando posicionarse en el directorio $HOME.
  ```bash
  cd ~
  ```
  > El símbolo `~` nos traslada directamente a la ruta definida en la variable de entorno $HOME
  
  ---
 
  ### 14.Verificar que se está en él.
  ```bash
  pwd
  ```
  ---

  ### 15.Listar todos los ficheros del directorio HOME mostrando sus permisos.
  ```bash
  ls -la /home
  ```
  > El parámetro `-l` permite mostrar la información en formato detallado, incluyendo permisos.
  > El parámetro `-a` permite mostrar también los archivos ocultos.
  ---
    
  ### 16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.
  ```bash
  rm -r /tmp/PRUEBA/*
  ```
  > El parámetro `-r` se utiliza para eliminar directorios de forma recursiva, es decir, borrar una carpeta y todo su contenido.
  ---

  ### 17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.
  
  ```bash
  mkdir /tmp/PRUEBA/{dir1,dir2,dir3}
  mkdir /tmp/PRUEBA/dir1/dir11
  mkdir /tmp/PRUEBA/dir3/dir31
  mkdir /tmp/PRUEBA/dir3/dir31/{dir311,dir312}
  ```
  > La expansión de llaves '{dir1,dir2}', es una funcionalidad que expande múltiples argumentos en una sola posición. Evita tener que escribir la ruta completa dos veces.
  
  **Alternativa una sola línea de comando:** 
  
  `mkdir -p /tmp/PRUEBA/{dir1/dir11,dir2,dir3/dir31/{dir311,dir312}}`

  > El parámetro -p (parents) crea automáticamente toda la ruta de directorios padres faltantes de una sola vez y no devuelve error si la carpeta ya existía.
  ---

  ### 18.Copiar el archivo /etc/mtab a vuestro directorio PRUEBA.
  ```bash
  cp -r /etc/mtab /tmp/PRUEBA/
  ```
    
  ### 19.Copiar /etc/mtab en dir1, dir2 y dir3.
  ```bash
  cp -r /etc/mtab /tmp/PRUEBA/dir1
  cp -r /etc/mtab /tmp/PRUEBA/dir2
  cp -r /etc/mtab /tmp/PRUEBA/dir3
  ```
  ---
    
  ### 20.Comprobar el ejercicio anterior mediante un solo comando.
  ```bash
  ls -R /tmp/PRUEBA
  ```
  > **Alternativa mediante búsqueda:** `find /tmp/PRUEBA -name 'mtab'`
  ---
  
