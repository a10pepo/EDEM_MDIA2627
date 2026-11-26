# Lab 4 · Rendimiento e índices

**10 minutos.** Compara el plan de una consulta en `terra_taronja` antes y después de crear un índice B-tree. Usa la [conexión `psql` del Lab 3](../lab03/README.md) y cierra las transacciones que sigan abiertas.

1. Ejecuta [01_generar_pedidos.sql](01_generar_pedidos.sql) completo. Añade `created_at`, genera **50.000** pedidos sintéticos con IDs del `1000000` al `1049999` y ejecuta `ANALYZE`. La comprobación debe mostrar **137** pedidos del 1 de abril de 2026. Los pedidos anteriores conservan su `order_date`.
2. Ejecuta [02_consulta_y_plan.sql](02_consulta_y_plan.sql) y anota el plan **antes**.
3. Ejecuta [03_crear_indice.sql](03_crear_indice.sql). Vuelve a ejecutar el mismo `02` y anota el plan **después**.

## Qué comparar y qué significa

1. **Filas devueltas.** Busca `actual ... rows=137` en el nodo superior de ambos planes. Es el recuento observado al ejecutar la consulta. El `rows` que aparece junto a `cost` es la estimación de PostgreSQL antes de ejecutarla.
2. **Cómo encontró esas filas.** `Seq Scan` recorre la tabla y aplica el filtro a medida que lee. `Rows Removed by Filter` cuenta las filas que examinó y descartó. Si después aparece `Bitmap Index Scan`, PostgreSQL usó el índice para localizar filas candidatas y `Bitmap Heap Scan` leyó sus páginas en la tabla. También puede usar `Index Scan`. Busca `idx_orders_created_at` para reconocer el índice de la práctica.
3. **Cuántos bloques consultó.** En el `Buffers` del nodo superior, `shared hit` indica bloques encontrados en la memoria de PostgreSQL y `shared read` indica bloques que tuvo que cargar. Compara la suma de ambos entre planes. El nodo superior ya incluye los accesos de los nodos que cuelgan de él.
4. **Cuánto tardó.** `Planning Time` es el tiempo para elegir el plan. `Execution Time` mide su ejecución. La caché y la carga de la instancia pueden cambiar los tiempos entre pasadas.

En la prueba local se devolvieron las mismas **137 filas**. El plan pasó de `Seq Scan` a `Bitmap Index Scan` con `Bitmap Heap Scan`, y los accesos a búferes bajaron de **319 a 140**. Eso muestra que PostgreSQL encontró el mismo resultado consultando menos bloques en esa ejecución. Si en tu instancia los dos planes muestran `Seq Scan`, el optimizador siguió prefiriendo escanear la tabla. Un índice no garantiza una mejora de tiempo. El objetivo es observar la decisión del optimizador. [Interpretar `EXPLAIN`](https://www.postgresql.org/docs/16/using-explain.html)

Contrasta tus resultados con la [comparación comentada de los planes](solucion/README.md).

## Repetir el experimento

Si quieres volver al punto de partida, ejecuta [04_limpiar.sql](04_limpiar.sql) y luego empieza por `01`. El script retira los pedidos sintéticos, `created_at` y el índice de la práctica. Si `psql` indica que hay una transacción abortada, ejecuta `ROLLBACK;` antes de limpiar.

## Cierre del curso

Cuando hayas terminado todos los labs, elimina `terra-taronja-lab1`. **Esto borra la instancia, la base `terra_taronja` y todos sus datos.**

1. Sal de todas las sesiones `psql` con `\q`, cierra Cloud SQL Studio y detén el proxy con `Ctrl+C` en su pestaña.
2. Abre la carpeta `SQL` de la misma copia que usaste para desplegar el Lab 1. Entra en el directorio del Lab 1, donde guardaste `terraform.tfvars` y `terraform.tfstate`. Comprueba que el `project_id` corresponde a tu proyecto del curso y revisa el plan de borrado.

   ```sh
   cd cloudSQL/lab01
   terraform state list
   terraform plan -destroy
   ```

3. Si el plan muestra la base `terra_taronja` y la instancia `terra-taronja-lab1` de tu proyecto, ejecuta el borrado y confirma con `yes` después de revisar el resumen. [Referencia de `terraform destroy`](https://developer.hashicorp.com/terraform/cli/commands/destroy)

   ```sh
   terraform destroy
   ```

4. Espera a que termine. Comprueba que `terraform state list` queda vacío y que `terra-taronja-lab1` desaparece de **Cloud SQL → Instancias** en tu proyecto. Puedes comprobarlo también con `gcloud sql instances list --project=PROJECT_ID`, sustituyendo `PROJECT_ID` por tu ID. En **Cloud SQL → Copias de seguridad**, verifica que no quedaron copias retenidas ni finales de esa instancia. [Eliminar instancias de Cloud SQL](https://docs.cloud.google.com/sql/docs/postgres/delete-instance) · [Copias de instancias eliminadas](https://docs.cloud.google.com/sql/docs/postgres/backup-recovery/manage-backups-deleted-instance)
