# Lab 2 · Modelo relacional y primeras consultas SQL

**Duración aproximada de 40 minutos.** Vas a crear las cinco tablas de Terra Taronja, cargar los datos de la tienda y consultar los importes de los pedidos en Cloud SQL Studio. La base `terra_taronja` y la instancia `terra-taronja-lab1` vienen del [Lab 1](../lab01/README.md).

## 1. Conéctate a Cloud SQL Studio · 5 min

1. En la consola de Google Cloud, selecciona tu proyecto individual y abre **Cloud SQL → Instancias → terra-taronja-lab1 → Cloud SQL Studio**.
2. Elige la base `terra_taronja` y la autenticación integrada. Usa el usuario `postgres` y la contraseña que configuraste en el Lab 1.
3. Ejecuta `SELECT current_database();`. Confirma que devuelve `terra_taronja` antes de ejecutar los scripts.

Abre en el repositorio los archivos `.sql` indicados en cada paso y copia su contenido en una pestaña de Studio. Escribe tus sentencias en los archivos de ejercicios antes de pulsar **Ejecutar**. Para probar una parte del archivo, selecciona las sentencias correspondientes y usa **Ejecutar selección**. Studio inicia una sesión por ejecución. Selecciona juntas todas las sentencias de un bloque que empiece con `BEGIN` y termine con `COMMIT` o `ROLLBACK`. Si hay varios resultados, elige el que quieres ver en el desplegable de resultados. [Usar Cloud SQL Studio](https://docs.cloud.google.com/sql/docs/postgres/manage-data-using-studio)

## 2. Diseña las tablas y carga los datos · 13 min

1. Abre [01_crear_tablas.sql](01_crear_tablas.sql). El enunciado indica qué columnas, tipos y restricciones debe tener cada tabla. Escribe tus cinco sentencias `CREATE TABLE` debajo de los bloques correspondientes.
2. Ejecuta tu SQL en el orden indicado. Crea cada tabla referenciada antes de la que contiene la clave foránea. Guarda tu SQL para poder volver a usarlo si reinicias el lab.
3. Actualiza el explorador de Studio y comprueba que el esquema `public` muestra las cinco tablas.
4. Ejecuta completo [02_datos_iniciales.sql](02_datos_iniciales.sql). Carga a María y Juan, seis productos y cuatro pedidos (`1001` a `1004`).

| Tabla | Clave primaria | Relaciones y restricciones |
| --- | --- | --- |
| `customers` | `customer_id` | Un cliente puede hacer varios pedidos. Cada correo es obligatorio y único. |
| `products` | `product_id` | `price` guarda el precio actual en euros y debe ser mayor o igual a cero. |
| `orders` | `order_id` | `customer_id` apunta a `customers`. Cada pedido tiene un cliente y una fecha. |
| `order_items` | `(order_id, product_id)` | Sus claves foráneas apuntan a `orders` y `products`. Solo hay una línea para cada producto dentro de un pedido. La cantidad es positiva y el precio histórico es mayor o igual a cero. |
| `inventory` | `product_id` | La misma columna apunta a `products`. Hay como máximo una fila de inventario por producto. El stock puede llegar a cero. |

La clave primaria identifica una fila. Una clave foránea exige que la fila a la que apunta exista.

## 3. Lee y modifica el catálogo · 4 min

Abre [03_consultas_ejemplo.sql](03_consultas_ejemplo.sql) y ejecuta los ejemplos en orden. Verás el catálogo y el cliente de cada pedido. El cálculo `SUM(quantity * unit_price)` da estos importes.

| Pedido | Cliente | Total |
| --- | --- | ---: |
| `1001` | María | 17,00 € |
| `1002` | Juan | 11,00 € |
| `1003` | María | 9,00 € |
| `1004` | Juan | 6,50 € |

El **precio actual** está en `products.price` y se usa para consultar el catálogo. El **precio histórico** está en `order_items.unit_price` y registra el importe unitario de esa compra. Calcula el total de un pedido con el precio histórico de cada línea.

En el ejemplo de `UPDATE`, selecciona de `BEGIN` a `ROLLBACK` y ejecuta todo el bloque junto. La naranja aparece a **6,00 €** en el catálogo, mientras que los pedidos `1001` y `1004` conservan sus precios de **5,50 €** y **2,50 €**. Al final, `ROLLBACK` devuelve el precio de catálogo a **2,50 €**. [ROLLBACK en PostgreSQL](https://www.postgresql.org/docs/16/sql-rollback.html)

## 4. Resuelve ocho ejercicios · 15 min

Abre [04_ejercicios.sql](04_ejercicios.sql), escribe tu SQL debajo de cada pregunta y ejecuta tu respuesta en Studio. En el último ejercicio, ejecuta el bloque completo con `BEGIN` y `ROLLBACK`, como en el ejemplo, para recuperar el precio original.

| Ejercicio | Resultado esperado |
| --- | --- |
| 1. Productos de más de 4 € | Zumo a 8,00 € y caja de naranjas de temporada a 12,00 €. |
| 2. Compras de Juan | En `1002`, un zumo a 3,00 € y dos mermeladas a 4,00 € por unidad. En `1004`, una naranja a 2,50 € y dos unidades de arroz a 2,00 € cada una. |
| 3. Gasto por cliente | María 26,00 € y Juan 17,50 €. |
| 4. Productos con poco stock | Queda una caja de naranjas de temporada. |
| 5. Importes del pedido `1001` | Naranja 11,00 € y zumo 6,00 €. |
| 6. Unidades vendidas | Naranja 3, zumo 3, mermelada 2, caja de temporada 0, horchata 2 y arroz 3. |
| 7. Pedido más caro | Pedido `1001` de María por 17,00 €. |
| 8. Oferta del zumo | Catálogo 3,50 € y precio histórico 3,00 € en `1001` y `1002`. Tras `ROLLBACK`, el catálogo vuelve a 8,00 €. |

## 5. Comprueba los resultados · 3 min

Ejecuta [06_comprobaciones.sql](06_comprobaciones.sql) al terminar. Los tres resultados deben mostrar `correcto = true` en todas las filas.

- `customers`, `products`, `orders`, `order_items` e `inventory` contienen 2, 6, 4, 8 y 6 filas, respectivamente.
- Los cuatro totales coinciden con la tabla del paso 3.
- El producto 4 tiene **una unidad** disponible. Déjala para el ejercicio del Lab 3 y conserva la instancia y la base de datos. El borrado de la instancia está previsto para el Lab 4.

Después de resolver la práctica, puedes consultar la [solución del modelo](solucion/01_solucion.sql) y las [ocho consultas resueltas](solucion/04_solucion.sql).

## Reinicio opcional

Reinicia solo si quieres repetir el Lab 2 desde cero y puedes perder todos los datos de sus cinco tablas. Comprueba en Studio que estás en tu proyecto, en la instancia `terra-taronja-lab1` y en la base `terra_taronja`. Si ya empezaste el Lab 3, el reinicio también eliminaría los cambios que hayas hecho en esas tablas.

1. Ejecuta completo [07_reiniciar_lab.sql](07_reiniciar_lab.sql). El script comprueba el nombre de la base antes de borrar las cinco tablas del esquema `public`. Si encuentra dependencias externas, `RESTRICT` bloquea el borrado.
2. Ejecuta de nuevo tus sentencias `CREATE TABLE` del paso 2. Después ejecuta `02_datos_iniciales.sql` y `06_comprobaciones.sql`, en ese orden. [DROP TABLE en PostgreSQL](https://www.postgresql.org/docs/16/sql-droptable.html)
