# Ejercicio Final: Pipeline de Datos Seguro y Automatizado

## 1. Activación manual
Al pulsar *Run workflow* se elige si ejecutar los Tests de Seguridad.

![](capturas/01_run_workflow_input.png)

## 2. Resumen de la ejecución
Los cuatro jobs terminan bien. La matrix lanza el procesamiento en staging y production.

![](capturas/02_resumen_ejecucion.png)

## 3. Tests de seguridad activados ("si")
Se valida el JSON y se ejecuta el escaneo de seguridad.

![](capturas/03_ci_seguridad_si.png)

## 4. Tests de seguridad desactivados ("no")
Se valida el JSON, pero el escaneo se salta.

![](capturas/04_ci_seguridad_no.png)

## 5. Artefactos
Un reporte por entorno, disponible para descargar.

![](capturas/05_artifacts.png)

## 6. Notificación de éxito
El secreto `DISCORD_WEBHOOK` aparece enmascarado como `***`.

![](capturas/06_notificacion_secreto.png)