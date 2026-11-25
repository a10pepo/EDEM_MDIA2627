# Lab 4 · Comparación comentada de los planes

El objetivo de los 10 minutos es observar cómo un índice cambia las opciones del optimizador para la misma consulta. La práctica carga 50.000 pedidos con `generate_series()`, repartidos por los 365 días de 2026. El rango del 1 de abril devuelve 137 filas, aproximadamente el 0,27 % de los pedidos sintéticos. Ese volumen bastó para observar un cambio de plan con la configuración predeterminada de PostgreSQL 16.16.

## Qué observar en los dos planes

| Métrica | Qué comparar |
| --- | --- |
| Tipo de escaneo | Busca `Seq Scan`, `Index Scan` o `Bitmap Heap Scan` con un `Bitmap Index Scan`. Si el índice participa, identifica `idx_orders_created_at` y el rango en `Index Cond`. |
| Filas estimadas y reales | Compara `rows` estimado con `actual rows`. La consulta debe devolver 137 filas en ambas ejecuciones. Revisa también `Rows Removed by Filter` cuando aparezca. |
| `Buffers` | Compara `shared hit` y `shared read` del nodo principal de ejecución. Sus totales ya incluyen el trabajo de sus hijos. Un `shared read` es una lectura hacia los búferes de PostgreSQL que puede satisfacerse desde la caché del sistema operativo. |
| Tiempos | Registra `Planning Time` y `Execution Time` por separado, en milisegundos. La carga, `ANALYZE`, la primera consulta y la creación del índice pueden cambiar qué páginas quedan en caché. |

PostgreSQL estima el coste de cada plan con las estadísticas de `ANALYZE`. Puede elegir `Seq Scan` con el índice presente si estima que leer secuencialmente sale más barato. El acceso por índice puede requerir leer también páginas de la tabla. Crear el índice no garantiza una mejora de tiempo. Compara primero el plan y las filas, y usa los tiempos como una observación local de esta demostración. Un benchmark profesional requeriría repetir las mediciones y controlar sus condiciones. [Uso de `EXPLAIN`](https://www.postgresql.org/docs/16/using-explain.html) · [Estadísticas de `ANALYZE`](https://www.postgresql.org/docs/16/sql-analyze.html)

## Resultado observado en PostgreSQL 16.16 local

La prueba usó los cuatro pedidos del Lab 2 y los 50.000 sintéticos. El servidor mantuvo sus opciones predeterminadas de escaneo. Las cifras ilustran una ejecución concreta.

| | Antes | Después |
| --- | --- | --- |
| Plan | `Seq Scan` | `Bitmap Heap Scan` con `Bitmap Index Scan` sobre `idx_orders_created_at` |
| Filas reales | 137 | 137 |
| Filas descartadas por el filtro | 49.867 | Sin línea `Rows Removed by Filter` |
| Búferes de ejecución | 319 `hit` | 137 `hit`, 3 `read` |
| `Planning Time` | 0,564 ms | 0,550 ms |
| `Execution Time` | 8,203 ms | 0,387 ms |

La lectura de esta salida empieza por las 137 filas, que coinciden en ambos planes. El `Seq Scan` recorrió la tabla y descartó las demás con `Filter`. El segundo plan usó la condición de fechas en `Index Cond` para localizar candidatos y consultar sus páginas. El nodo principal pasó de 319 accesos a búferes a 140. El tiempo bajó en esa ejecución. Si el tipo de escaneo coincide en dos pases pero el tiempo cambia, revisa los `hit` y `read` antes de atribuir el cambio al índice.

## Repetición y limpieza

`orders` ya tiene `order_date`. La preparación añade `created_at` para los datos de esta práctica y conserva los campos de los pedidos anteriores. La carga se detiene si el rango de IDs está ocupado, y la definición de la columna y del índice queda marcada para identificarla durante la limpieza.

Para repetir la comparación, ejecuta `04`, después `01` y sigue el orden de la [guía del lab](../README.md). La limpieza quita el índice, los pedidos sintéticos y `created_at`. Si detecta que otra fila usa la columna, que existe un índice ajeno con el mismo nombre o que otros objetos dependen de la columna, se detiene y conserva el estado. Las claves foráneas también protegen las líneas que pudieran referenciar un pedido sintético. [Script de limpieza](../04_limpiar.sql)

Al terminar, sigue el [cierre del bloque](../README.md#cierre-del-curso) para borrar la instancia y verificar el resultado en tu proyecto.
