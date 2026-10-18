# EJERCICIOS LINUX

## 1. Listar todos los archivos del directorio `bin`

```bash
ls /bin/
```

## 2. Listar todos los archivos del directorio `tmp`

```bash
ls /tmp/
```

## 3. Listar todos los archivos del directorio `etc` que empiecen por `t`

```bash
ls /etc/t*
```

## 4. Listar todos los archivos del directorio `dev` que empiecen por `tty`

```bash
ls /dev/tty*
```

## 5. Listar todos los archivos del directorio `dev` que empiecen por `tty` y acaben en `3`

```bash
ls /dev/tty*3
```

## 6. Listar todos los archivos del directorio `dev` que empiecen por `t` y acaben en `C1`

```bash
ls /dev/t*C1
```

## 7. Listar todos los archivos, incluidos los ocultos, del directorio raíz

```bash
ls -a /
```

## 8. Listar todos los archivos del directorio `etc` que no empiecen por `t`

```bash
ls /etc/[!t]*
```

## 9. Listar todos los archivos del directorio `usr` y sus subdirectorios

```bash
find /usr/ -maxdepth 1 -type f,d
```

## 10. Cambiarse al directorio `tmp` y crear el directorio `PRUEBA`

```bash
cd /tmp/
mkdir PRUEBA
```

## 11. Verificar que el directorio actual ha cambiado

```bash
ls
```

## 12. Mostrar el día y la hora actual

```bash
date
```

## 13. Con un solo comando posicionarse en el directorio `$HOME`

```bash
cd $HOME
```

## 14. Verificar que se está en él

```bash
pwd
```

## 15. Listar todos los ficheros del directorio `HOME` mostrando sus permisos

```bash
ls -l $HOME
```

## 16. Borrar todos los archivos y directorios visibles del directorio `PRUEBA`

```bash
rm -r /tmp/PRUEBA/*
```

## 17. Crear la estructura de directorios indicada

Crear los directorios `dir1`, `dir2` y `dir3` dentro de `PRUEBA`. Dentro de `dir1`, crear `dir11`. Dentro de `dir3`, crear `dir31` y, dentro de este, crear `dir311` y `dir312`.

```bash
mkdir /tmp/PRUEBA/dir1 /tmp/PRUEBA/dir2 /tmp/PRUEBA/dir3
mkdir /tmp/PRUEBA/dir1/dir11
mkdir /tmp/PRUEBA/dir3/dir31
mkdir /tmp/PRUEBA/dir3/dir31/dir311 /tmp/PRUEBA/dir3/dir31/dir312
```


## 18. Copiar el archivo `/etc/mtab` al directorio `PRUEBA`

```bash
cp /etc/mtab /tmp/PRUEBA/
```

## 19. Copiar `/etc/mtab` en `dir1`, `dir2` y `dir3`

```bash
cp /etc/mtab /tmp/PRUEBA/dir1
cp /etc/mtab /tmp/PRUEBA/dir2
cp /etc/mtab /tmp/PRUEBA/dir3
```

## 20. Comprobar el ejercicio anterior mediante un solo comando

```bash
find /tmp/PRUEBA/
```