# Lab 3 · Transacciones y concurrencia

**Duración aproximada de 40 minutos.** Usa la instancia `terra-taronja-lab1`, la base `terra_taronja` y las cinco tablas con los datos del [Lab 2](../lab02/README.md). La naranja (producto `1`) tiene 24 unidades y la caja de temporada (producto `4`) tiene una. Los pedidos `2001` a `2004` quedan reservados para esta práctica.

## 1. Abre dos sesiones PostgreSQL · 8 min

Cloud SQL Studio inicia una sesión nueva en cada ejecución. Aquí necesitas dos conexiones que permanezcan abiertas entre `BEGIN` y `COMMIT` o `ROLLBACK`. Usarás dos clientes `psql` desde Cloud Shell. [Límites de las sesiones de Cloud SQL Studio](https://docs.cloud.google.com/sql/docs/postgres/manage-data-using-studio#limitations)

### Pestaña del proxy

1. Selecciona tu proyecto individual en la consola de Google Cloud y abre **Cloud Shell**. Acepta la autorización si aparece. Cloud Shell incluye `gcloud` y `psql`. [Conexión desde Cloud Shell](https://docs.cloud.google.com/sql/docs/postgres/debugging-connectivity)
2. Sustituye `ID_DE_TU_PROYECTO` por el ID real y obtén el nombre de conexión. Debe tener el formato `proyecto:región:terra-taronja-lab1`.

   ```bash
   PROJECT_ID='ID_DE_TU_PROYECTO'
   CONNECTION_NAME="$(gcloud sql instances describe terra-taronja-lab1 \
     --project="$PROJECT_ID" --format='value(connectionName)')"
   printf '%s\n' "$CONNECTION_NAME"
   ```

3. Descarga el Cloud SQL Auth Proxy para Cloud Shell Linux x86-64. Deja el proxy ejecutándose en esta pestaña y espera a que indique que escucha en `127.0.0.1:5433`. [Instalación y uso del proxy](https://docs.cloud.google.com/sql/docs/postgres/connect-auth-proxy)

   ```bash
   mkdir -p "$HOME/.local/bin"
   curl -fL 'https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.28.0/cloud-sql-proxy.linux.amd64' \
     -o "$HOME/.local/bin/cloud-sql-proxy"
   chmod +x "$HOME/.local/bin/cloud-sql-proxy"
   "$HOME/.local/bin/cloud-sql-proxy" --address 127.0.0.1 --port 5433 "$CONNECTION_NAME"
   ```

El Lab 1 tiene IPv4 pública, conexiones cifradas y la lista de redes autorizadas vacía. El proxy usa la IPv4 pública y cifra el tramo hasta Cloud SQL. Mantén la lista de redes autorizadas vacía. El proxy usa tu identidad de Google Cloud y necesita `cloudsql.instances.get` y `cloudsql.instances.connect`. El rol **Cloud SQL Admin** del Lab 1 ya incluye ambos permisos. **Cloud SQL Client** basta para conectarse a una instancia ya desplegada. [Red y cifrado del proxy](https://docs.cloud.google.com/sql/docs/postgres/sql-proxy) · [Roles de Cloud SQL](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudsql)

### Pestañas A y B

En el panel de **esa misma Cloud Shell**, pulsa dos veces **Añadir sesión de Cloud Shell (+)**. Las pestañas comparten la VM y el proxy local. Abre `psql` en cada una con el mismo comando e introduce la contraseña de `postgres` del Lab 1 cuando te la pida. María y Juan son clientes de la tienda que representarás desde esas sesiones. [Varias terminales de Cloud Shell](https://docs.cloud.google.com/shell/docs/use-cloud-shell-terminal#open_multiple_terminal_sessions)

```bash
psql -X -W 'host=127.0.0.1 port=5433 dbname=terra_taronja user=postgres sslmode=disable'
```

`sslmode=disable` se aplica al tramo local entre `psql` y el proxy en la misma VM. El proxy abre el túnel cifrado hasta Cloud SQL. [Conexiones del proxy](https://docs.cloud.google.com/sql/docs/postgres/sql-proxy)

1. En A y B, ejecuta `SELECT current_database(), pg_backend_pid();`. Debe aparecer `terra_taronja` en ambas y un PID distinto en cada una. Apunta los PID para identificar quién bloquea a quién.
2. En A, pega y ejecuta [00_comprobar_inicio.sql](00_comprobar_inicio.sql). Los stocks deben ser 24 y 1, y las columnas de comprobación deben mostrar `t`. Si falla algo, detente y comprueba con el profesor los datos del Lab 2 o si ha quedado una ejecución anterior.

Copia un bloque de SQL cada vez al prompt de `psql`. Espera a ver el resultado antes de seguir al paso siguiente.

## 2. Experimento A · COMMIT y ROLLBACK · 5 min

Usa la pestaña A y los bloques de [01_a_commit_rollback.sql](01_a_commit_rollback.sql).

1. Ejecuta **A1**. `RETURNING` muestra que la naranja tiene 23 unidades dentro de la transacción. **Detente** antes de ejecutar `ROLLBACK`. En B, ejecuta `SELECT stock FROM public.inventory WHERE product_id = 1;`. Todavía verás el stock confirmado de 24.
2. Ejecuta **A2** en A. El stock vuelve a 24.
3. Ejecuta **A3** y después **A4**. Vuelves a ver 23 unidades dentro de la transacción y, tras el `COMMIT`, la consulta sigue mostrando 23. La caja de temporada conserva su unidad.

## 3. Experimento B · Una compra confirmada y una fallida · 10 min

Sigue en la pestaña A y abre [02_b_compras.sql](02_b_compras.sql). Trabaja un paso cada vez. El archivo ya incluye `BEGIN`, `COMMIT`, `ROLLBACK` y las consultas de comprobación al final de cada compra. Completa los `SELECT` de stock y precio, los `INSERT` y el `UPDATE` donde se indica. Ejecuta cada sentencia en su turno y revisa el resultado antes de pasar a la siguiente.

1. Consulta el stock en `inventory`.
2. Crea el pedido en `orders` y su línea en `order_items`. Guarda en la línea el precio actual de `products`.
3. Descuenta las unidades en `inventory`.
4. Confirma si se hizo el descuento. Si la compra falla, revierte toda la transacción.

**Primero, compra confirmada (B1 a B8).** Juan pide una naranja. Comprueba que quedan `23` y consulta su precio actual. Registra el pedido `2004` y su línea. Tras el descuento, espera `UPDATE 1` y stock `22`. Ejecuta el `COMMIT` de B7 y las comprobaciones de B8. Si el descuento falla, ejecuta `ROLLBACK;` y revisa el resultado antes de continuar.

**Después, compra fallida (B9 a B16).** María pide dos cajas. Comprueba que queda una y consulta el precio. Registra el pedido `2001` y su línea e intenta restar dos unidades en B14 para provocar el error del `CHECK`. Detente para leerlo y ejecuta el `ROLLBACK` de B15. Las comprobaciones de B16 deben mostrar que el pedido y su línea se deshicieron y que sigue quedando una caja. Si el descuento termina sin error, revierte la transacción y revisa el stock y la restricción del Lab 2.

## 4. Experimento C · Dos compradores y una caja · 14 min

Abre los enunciados de la [sesión A](03_c_sesion_a.sql) y la [sesión B](03_c_sesion_b.sql). Cada archivo trae `SET application_name` y `BEGIN`. En ambas sesiones reutiliza **B2 a B5 del `02`** para consultar stock y precio e insertar el pedido y su línea. En A usa el descuento condicional de B6. En B usa el descuento de B14, restando una sola unidad y filtrando solo por el ID del producto. Mantén la lectura de stock con un `SELECT` normal para que la espera ocurra al intentar descontar la caja.

| Paso | Sesión | Qué hacer y observar |
| --- | --- | --- |
| **C1** | A · María | Abre la transacción y aplica B2 a B6 al pedido `2002`. Lee stock `1` y precio `12 €`. El descuento devuelve `UPDATE 1` y stock `0`. **Detente antes de confirmar.** |
| **C2** | B · Juan | Abre la transacción y aplica B2 a B5 al pedido `2003`. B también lee stock `1` y precio `12 €`. Intenta descontar una unidad como en B14. **B se queda esperando.** Cambia a A. |
| **C3** | A · María | Ejecuta la consulta de diagnóstico. B debe figurar con `wait_event_type = Lock` y con el PID de A entre los bloqueadores. |
| **C4** | A · María | Si viste `UPDATE 1` en C1 y la transacción sigue abierta, confirma la compra con el `COMMIT` de B7. B se desbloquea. |
| **C5** | B · Juan | El descuento falla con un `ERROR` por violar la restricción `CHECK` del stock (`23514`). Reutiliza el `ROLLBACK` de B15 y comprueba que el pedido `2003` y su línea desaparecieron. |

Ambos leen `1` al empezar sus compras porque el descuento de A sigue pendiente cuando B consulta. En `READ COMMITTED`, el `UPDATE` de B retoma la fila ya confirmada por A, con stock `0`. Al restar una unidad, intenta escribir `-1`. El `CHECK (stock >= 0)` aborta la transacción de B. Ejecuta `ROLLBACK` para deshacer también el pedido y la línea. [Aislamiento en PostgreSQL](https://www.postgresql.org/docs/16/transaction-iso.html#XACT-READ-COMMITTED)

## 5. Comprueba y restaura · 3 min

1. Con ambas transacciones cerradas, ejecuta en A [04_comprobar_resultado.sql](04_comprobar_resultado.sql). El stock de la naranja debe ser **22** y el de la caja **0**. Quedan el pedido **`2004` de Juan**, por una naranja a **2,50 €**, y el **`2002` de María**, por una caja a **12 €**. Se vendió una sola caja y los pedidos `2001` y `2003` no aparecen.
2. Ejecuta completo [05_restaurar.sql](05_restaurar.sql). Se eliminan los pedidos de prueba y sus líneas, y los stocks de los productos `1` y `4` vuelven a 24 y 1. Ejecuta [00_comprobar_inicio.sql](00_comprobar_inicio.sql) para verificarlo.
3. Sal de A y B con `\q`. Detén el proxy con `Ctrl+C` en su pestaña. Conserva la instancia para el Lab 4.

Si se interrumpe el ejercicio C, cancela la consulta que esté esperando en B con `Ctrl+C` y ejecuta `ROLLBACK` en las sesiones que sigan abiertas antes de restaurar. Ejecuta la restauración solo en tu base de prácticas y con los IDs de prueba reservados para este lab.

Después de hacer la práctica, compara tus resultados con las [soluciones y comprobaciones](solucion/README.md).
