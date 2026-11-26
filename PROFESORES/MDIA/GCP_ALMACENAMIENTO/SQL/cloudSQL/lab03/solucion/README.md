# Lab 3 · Soluciones y resultados

La sesión dura unos 40 minutos. Reserva tiempo para abrir el proxy y comprobar los dos PID antes de iniciar las transacciones. Durante el experimento C, deja a B esperando hasta que el grupo haya visto el bloqueo en el terminal o en `pg_stat_activity`.

## Preparación

- Necesitas la instancia del [Lab 1](../../lab01/README.md), las tablas y datos del [Lab 2](../../lab02/README.md) y la contraseña de `postgres`. El stock de la naranja (`1`) debe ser `24` y el de la caja (`4`), `1`. Los identificadores `2001` a `2004` deben estar libres. [Comprobación inicial](../00_comprobar_inicio.sql)
- El proxy reutiliza la IPv4 pública con la lista de redes autorizadas vacía. La cuenta de Cloud Shell necesita `cloudsql.instances.get` y `cloudsql.instances.connect`, incluidos en **Cloud SQL Admin** y **Cloud SQL Client**. La Cloud SQL Admin API debe seguir habilitada. Confirma el acceso saliente del proxy por TCP `443` y `3307` si el entorno aplica restricciones de egreso. [Acceso con el proxy](https://docs.cloud.google.com/sql/docs/postgres/sql-proxy) · [Permisos de Cloud SQL](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudsql)
- Abre dos `psql` al mismo proxy según la [guía del lab](../README.md). Ambos deben devolver `terra_taronja` con PID distintos. Cada ejecución en Cloud SQL Studio inicia una sesión nueva, por lo que las pausas del ejercicio se hacen en `psql`. [Sesiones de Cloud SQL Studio](https://docs.cloud.google.com/sql/docs/postgres/manage-data-using-studio#limitations)

## Respuestas y resultados esperados

El [experimento A](../01_a_commit_rollback.sql) incluye el SQL completo. En B, compara las consultas de stock y precio, los `INSERT` y el `UPDATE` con la solución. En C se reutilizan B2 a B5 para ambos compradores, B6 para el descuento de A y B14 para el de B, adaptado a una unidad. Ejecuta los SQL resueltos por bloques y respeta las pausas para observar el bloqueo. [Solución de las compras de B](02_b_compras_solucion.sql) · [Solución de la sesión A](03_c_sesion_a_solucion.sql) · [Solución de la sesión B](03_c_sesion_b_solucion.sql)

| Experimento | Qué observar | Explicación |
| --- | --- | --- |
| A · `ROLLBACK` | A ve `23` después del `UPDATE`. B sigue viendo `24`. Tras el `ROLLBACK`, A también ve `24`. | Una sesión ve sus propios cambios pendientes. Una lectura normal en B ve el último estado confirmado. |
| A · `COMMIT` | El segundo `UPDATE` vuelve a mostrar `23`. Tras el `COMMIT`, A y B pueden leer `23`. | El cambio confirmado queda persistido y visible para otras sesiones. |
| B · Compra confirmada (B1 a B8) | Se leen `23` naranjas y precio `2,50 €`. Se insertan el pedido `2004` de Juan y su línea. El descuento devuelve `UPDATE 1` y stock `22`. Tras `COMMIT`, el pedido, la línea y el nuevo stock quedan guardados. | El pedido y el descuento se confirman juntos. La caja conserva su última unidad para C. |
| B · Compra fallida (B9 a B16) | Se lee stock `1` y precio `12,00 €`. Se insertan el pedido `2001` y su línea de dos unidades. El descuento de B14 viola el `CHECK` (`23514`). Tras `ROLLBACK`, desaparecen las dos filas y queda una caja. | Una unidad menos las dos solicitadas da stock negativo. El error aborta la transacción y el `ROLLBACK` deshace también las escrituras previas. |
| C · Antes del `COMMIT` de A | A lee `1`, registra el pedido `2002` y su línea, y obtiene `UPDATE 1`. B también lee `1`, registra el pedido `2003` y su línea, y se bloquea al descontar. En C3 aparece `Lock` y el PID de A. | El `SELECT` de B ve el stock confirmado. El `UPDATE` de B espera a que A libere el bloqueo de la fila. |
| C · Después del `COMMIT` de A | B devuelve un error de `CHECK` (`23514`). El alumno hace `ROLLBACK` y comprueba que el pedido `2003` y su línea desaparecieron. El stock de la caja queda en `0` y el único pedido con una caja es el `2002` de María por `12,00 €`. | Bajo `READ COMMITTED`, B intenta restar una unidad del stock confirmado de `0`. El `CHECK` rechaza el valor `-1` y aborta la transacción. |

Pregúntales qué habría ocurrido si B hubiera reutilizado el filtro `stock >= 1` de A. Al terminar la espera, la fila con stock `0` quedaría fuera del `UPDATE` y el resultado sería `UPDATE 0`. Al filtrar solo por ID, el `CHECK` detecta el intento de dejar stock negativo. [Aislamiento y reevaluación de `WHERE`](https://www.postgresql.org/docs/16/transaction-iso.html#XACT-READ-COMMITTED)

## Incidencias y recuperación

| Síntoma | Comprobación |
| --- | --- |
| El proxy devuelve `403` o un error al obtener la instancia | Comprueba el proyecto, la cuenta de Cloud Shell, los permisos efectivos y la Cloud SQL Admin API. |
| `psql` no llega a `127.0.0.1:5433` | Confirma que el proxy sigue abierto y las tres pestañas pertenecen al mismo panel de Cloud Shell. Si el proxy indica un error de salida a la red, revisa TCP `443` y `3307`. |
| `password authentication failed` | Usa el usuario `postgres` y la contraseña de PostgreSQL del Lab 1. |
| El descuento de B14 termina sin error | Ejecuta `ROLLBACK`. Comprueba que el `UPDATE` filtra solo por producto, el stock inicial es `1` y `inventory` tiene `CHECK (stock >= 0)`. |
| B no espera o C3 no muestra bloqueo | Confirma que A obtuvo `UPDATE 1` y sigue con C1 sin confirmar. Verifica que C2 se ejecutó en el otro PID. Si A ya confirmó, recupera el estado antes de repetir. |
| El prompt muestra una transacción abortada | Lee el primer `ERROR` para identificar la causa. Si B sigue esperando, cancela su consulta con `Ctrl+C`. Ejecuta `ROLLBACK` en las sesiones abiertas antes de restaurar y repetir. |

Antes de restaurar, ejecuta [04_comprobar_resultado.sql](../04_comprobar_resultado.sql) y revisa los pedidos confirmados `2002` y `2004` y los stocks `22` y `0`. [05_restaurar.sql](../05_restaurar.sql) comprueba que la base sea `terra_taronja`, elimina los pedidos de prueba `2001` a `2004` y sus líneas, y restablece los dos stocks afectados. Ejecútalo con las transacciones cerradas y solo si esos identificadores se reservaron para el lab. Vuelve a ejecutar [00_comprobar_inicio.sql](../00_comprobar_inicio.sql) para confirmar la restauración. La instancia se conserva hasta el Lab 4.
