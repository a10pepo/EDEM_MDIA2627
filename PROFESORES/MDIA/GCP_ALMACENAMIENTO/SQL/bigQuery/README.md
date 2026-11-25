# BigQuery · Datos de Terra Taronja

El [Lab 1](./lab01/README.md) usa los CSV incluidos en `lab01/datos/`. El [Lab 2](./lab02/README.md) genera siete CSV en `salida/`. El [ejercicio final](./ejercicio_final/README.md) reutiliza el histórico cargado en el Lab 2. Los nombres de clientes son sintéticos y sus correos usan `@example.com`.

## Regenerar y validar

Abre una terminal en la carpeta `SQL`, que contiene `bigQuery`. Usa Python 3.10 o posterior.

```text
python -B -X utf8 bigQuery/generar_datos.py --output bigQuery/salida
python -B -X utf8 bigQuery/test_datos.py
```

El generador usa la semilla `27182` y crea **1.200.000 pedidos**. Usa `--scale 0.05` para un ensayo local con 60.000 pedidos. Las cifras de las soluciones corresponden al conjunto completo. Puedes regenerar los dos CSV del Lab 1 con `--small` y un directorio de salida independiente.

Las pruebas generan datos temporales y comprueban esquemas, fechas, referencias, conciliación de importes y consultas resueltas en SQLite. También puedes validar los CSV completos una vez generados.

```text
python -B -X utf8 bigQuery/test_datos.py --csv-dir bigQuery/salida --orders 1200000 --report
```

Si ya subiste los CSV a un bucket compatible con **EU**, puedes cargarlos con [02_cargar_gcs.sql](./lab02/sql/02_cargar_gcs.sql). El script espera los archivos bajo el prefijo `bigquery/` y reemplaza el contenido de las tablas indicadas. El flujo principal de la clase carga desde el equipo de cada alumno con `bq`.
