# Ejercicio final: Pipeline de datos seguro y automatizado

En este ejercicio he creado un workflow de GitHub Actions (`ejercicio_entregable.yaml`) que procesa un archivo de ventas en formato JSON. El workflow lo he probado en mi repositorio personal ([Marcosberna/ENTREGABLE_GITACTIONS](https://github.com/Marcosberna/ENTREGABLE_GITACTIONS)), porque GitHub solo ejecuta los workflows que están en la carpeta `.github/workflows/` de la raíz del repo. Aquí subo los archivos y las capturas de las ejecuciones.

## Archivos

- `ejercicio_entregable.yaml`: el workflow.
- `ventas.json`: los datos de ventas que se procesan.
- `scripts/security_scan.py`: script en Python que simula un escaneo de seguridad buscando claves API expuestas en los archivos del repo.
- `scripts/procesar_ventas.py`: script en Python que genera un reporte en .txt según el entorno (staging o production).
- `capturas/`: las capturas de las ejecuciones.

## Cómo funciona

El workflow se lanza de forma manual con `workflow_dispatch` y tiene un input llamado `tests_seguridad` en el que se elige "sí" o "no".

**Job 1 (CI & Seguridad):** se ejecuta en `ubuntu-latest`. Primero comprueba que `ventas.json` es un JSON válido con `python -m json.tool`. Después, solo si en el input se ha elegido "sí", ejecuta el script de seguridad. Si se ha elegido "no", se ejecuta otro paso que solo muestra un mensaje diciendo que el escaneo se ha omitido.

**Job 2 (Procesamiento):** depende del Job 1 con `needs`. Usa una matrix con los entornos `staging` y `production`, así que se crean dos jobs. Cada uno genera su propio reporte: el de staging incluye el detalle de cada venta y el de production es un resumen con el IVA aplicado. Al final los reportes se suben como artefactos con `actions/upload-artifact` para que se puedan descargar.

**Job 3 (Notificación de éxito):** depende de los dos jobs anteriores y solo se ejecuta si han terminado bien (`if: success()`). Usa el secreto `DISCORD_WEBHOOK`, que he creado en Settings > Secrets and variables > Actions, y simula el envío de la notificación con un `echo`. GitHub oculta el valor del secreto en los logs y lo muestra como `***`.

## Capturas

### 1. Lanzar el workflow eligiendo "sí"

![Activación manual con sí](capturas/01_activacion_manual_si.png)

Desde la pestaña Actions, en "Run workflow", aparece la pregunta de si quiero ejecutar los tests de seguridad. En esta ejecución elijo "sí".

### 2. Resumen de la ejecución

![Resumen del pipeline](capturas/02_resumen_pipeline.png)

La ejecución #2 ha terminado correctamente. En el diagrama se ve el orden de los jobs: primero el Job 1, luego los dos jobs de la matrix (staging y production) y por último el Job 3. Arriba también se ve que se han generado 2 artefactos. Los avisos amarillos son porque algunas acciones usan Node.js 20, que GitHub va a dejar de usar, pero no afectan al funcionamiento.

### 3. Job 1 con la validación y el escaneo

![Job 1 con validación y escaneo](capturas/03_job1_validacion_escaneo.png)

En el Job 1 se ve que el JSON es válido y que el escaneo de seguridad ha revisado los archivos sin encontrar ninguna clave expuesta. El paso de "Escaneo de seguridad omitido" aparece tachado porque no se ha ejecutado, ya que elegí "sí".

### 4. Artefactos

![Artefactos](capturas/04_artefactos.png)

Al final del resumen aparecen los dos reportes subidos como artefactos, `reporte-production` y `reporte-staging`. Tienen distinto tamaño porque el contenido de cada uno es diferente. Desde aquí el jefe de departamento podría descargarlos.

### 5. Job 3 con la notificación

![Job 3 notificación](capturas/05_job3_notificacion.png)

El Job 3 se ha ejecutado porque los anteriores terminaron bien. Usa el secreto `DISCORD_WEBHOOK` y en el log la URL aparece como `***`, porque GitHub enmascara los secretos.

### 6. Lanzar el workflow eligiendo "no"

![Activación manual con no](capturas/06_activacion_manual_no.png)

Vuelvo a lanzar el workflow, pero esta vez elijo "no" para comprobar que el condicional funciona.

### 7. Job 1 con el escaneo omitido

![Job 1 escaneo omitido](capturas/07_job1_escaneo_omitido.png)

En la ejecución #4, como elegí "no", el paso del escaneo de seguridad no se ejecuta (aparece tachado) y en su lugar se ejecuta el paso que muestra el mensaje "El usuario eligió NO ejecutar los Tests de Seguridad". Con esta captura y la número 3 se ve que el condicional funciona en los dos casos.
