# Evidencias de Ejecución - GitHub Actions
**Alumno:** Joaquín Villalobos

## 1. Disparo Manual e Inputs (`workflow_dispatch`)
Se configuró el evento `workflow_dispatch` para permitir la activación manual del flujo desde la interfaz de GitHub Actions, incluyendo el parámetro de entrada `security_tests` de tipo booleano (casilla de verificación).

![Formulario de disparo manual](disparador-manual.png)

---

## 2. Evaluación de Lógica Condicional (`if`)
El paso *Escaneo seguridad* evalúa la condición `if: inputs.security_tests == true`. 

* **Casilla desmarcada (`false`):** El motor de GitHub Actions omite el paso de escaneo (*Skipped*), continuando con el resto del job sin fallar.

![Paso de escaneo omitido](escaneo-seguridad==False.png)

* **Ejecución del Job de CI:** Al ejecutarse con normalidad, se valida la estructura del archivo `ventas.json` mediante `jq`.

![Logs del job ci_seguridad](job%20-%20seguridad.png)

---

## 3. Matriz de Ejecución en Paralelo (`matrix`)
El job `procesamiento` utiliza una estrategia de matriz para ejecutar de forma simultánea los entornos de `staging` y `production`.

![Job Procesamiento - Staging](job%20-%20procesamiento%20-%20staging.png)
![Job Procesamiento - Production](job%20-%20procesamiento%20-%20production.png)

---

## 4. Generación y Almacenamiento de Artefactos
Cada trabajo de la matriz genera un informe individualizado y lo sube al almacenamiento temporal de GitHub mediante la acción `actions/upload-artifact@v4`.

![Artefactos subidos](artifacts-generados.png)

---

## 5. Gestión de Secretos y Enmascaramiento
En el job `notification`, la variable de entorno toma la URL guardada en `secrets.DISCORD_WEBHOOK`. En la salida de consola se verifica el enmascaramiento automático (`***`), garantizando que los datos sensibles no queden expuestos en texto plano.

![Registro del job notification](job%20-%20notification.png)
![Enmascaramiento del Webhook](evidencia%20notificacion%20sin%20clave%20en%20claro.png)

---

## 6. Flujo Completo y Grafo de Dependencias (DAG)
Ejecución exitosa de los 3 jobs en secuencia (`ci_seguridad` $\rightarrow$ `Matrix: Procesamiento` $\rightarrow$ `notification`), cumpliendo con la dependencia `needs`.

![Resumen general del workflow](workflow-exitoso.png)