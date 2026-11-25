# BigLake · Lab 03 · Compara las ofertas de Terra Taronja

**30 minutos, incluida la limpieza final · BigQuery Studio**

Terra Taronja vende productos de la Comunitat Valenciana. Compras ya tiene tres catálogos y necesita decidir dónde pedir cada producto. Vas a comparar los precios y las existencias de A, B y C usando los mismos códigos internos y las mismas unidades de venta.

## 1. Prepara el entorno · 5 min

Usa tu proyecto de los Labs 01 y 02, en **EU**, y la misma copia del repositorio donde los desplegaste. El Lab 03 reutiliza los archivos que ya subiste a Cloud Storage, el dataset y la conexión. Su Terraform crea únicamente seis tablas externas en `terra_taronja_biglake`. Puedes hacer la práctica aunque ya hayas borrado las tablas que creaste a mano en los otros labs.

| Tablas del Lab 03 | Origen |
| --- | --- |
| `lab03_proveedor_a` y `lab03_proveedor_c` | CSV y Parquet del bucket del Lab 01. |
| `lab03_proveedor_b` | NDJSON del bucket restringido del Lab 02, leído mediante la conexión `terra_taronja_restringida`. |
| `lab03_productos`, `lab03_correspondencias` y `lab03_entregas` | CSV del catálogo interno, las correspondencias y el histórico de entregas del bucket del Lab 01. |

Abre PowerShell en `bigLake/lab03/terraform` dentro de `SQL`, donde está `main.tf`. Si el prompt ya termina en `lab03\terraform>`, ejecuta estos comandos ahí mismo.

```powershell
terraform init
terraform plan
```

El plan debe mostrar seis tablas `lab03_...` nuevas en tu proyecto. Si coincide, ejecuta el comando siguiente y escribe `yes`.

```powershell
terraform apply
```

Abre [BigQuery Studio](https://console.cloud.google.com/bigquery) con tu usuario habitual. En **Explorer → Datasets → terra_taronja_biglake**, busca las seis tablas. En **Details** de cada tabla de proveedor verás la dirección del archivo que lee. Si Terraform indica que falta un estado, comprueba que ejecutaste los dos labs anteriores en esta misma copia del repositorio.

## 2. Comprueba las tres fuentes · 2 min

En **SQL query**, cambia `TU_PROJECT_ID` por el valor de `project_id` que usaste en los labs anteriores. Pulsa **Run**. BigQuery cuenta las filas de cada archivo usando SQL. En los siguientes pasos, sigue los comentarios `-- Completa` antes de ejecutar cada bloque. Puedes comprobar tus consultas en la carpeta [`solucion`](./solucion/).

```sql
SELECT 'A' AS proveedor, 'CSV' AS formato, COUNT(*) AS ofertas
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_a`
UNION ALL
SELECT 'B', 'NDJSON', COUNT(*)
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b`
UNION ALL
SELECT 'C', 'Parquet', COUNT(*)
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_c`
ORDER BY proveedor;
```

Debes ver **16 ofertas por proveedor**. Abre **Schema** en las tres tablas. Busca cómo llama cada proveedor a su referencia, su precio y su stock.

## 3. Guarda la conversión a euros en una vista · 4 min

El precio de B viene en céntimos. Usa `CAST` para convertir el precio a `NUMERIC` y expresa el resultado en euros. Los alias dan a las columnas los nombres que usaremos para unir las ofertas.

En **SQL query**, sustituye `TU_PROJECT_ID` y completa la línea de `price_eur`. Ejecuta el bloque con **Run**. La vista guarda la consulta y BigQuery aplica la conversión cada vez que lees esa columna. [Vistas lógicas en BigQuery](https://docs.cloud.google.com/bigquery/docs/views-intro)

```sql
CREATE OR REPLACE VIEW `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur` AS
SELECT
  'B' AS supplier_id,
  product_code AS supplier_sku,
  description AS product_name,
  -- Completa la conversión de price_cents a euros. Sustituye esta expresión.
  CAST(NULL AS NUMERIC) AS price_eur,
  stock AS available_units
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b`;
```

Busca `lab03_proveedor_b_eur` en **Explorer** y consulta una referencia para comprobar la conversión.

```sql
SELECT supplier_sku, product_name, price_eur, available_units
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur`
WHERE supplier_sku = 'B-0135';
```

`B-0135` es la **Naranja de Carcaixent**, a **3,20 €** por bolsa de 1 kg. Tiene **0 bolsas** disponibles. En A el precio ya viene en euros. En C, Parquet guarda el precio como decimal y el stock como entero.

## 4. Une las ofertas y relaciónalas con el catálogo · 5 min

`UNION ALL` coloca las ofertas de los tres proveedores en una misma lista. Las columnas deben coincidir en posición y tipo. Para B, toma `price_eur` de la vista que acabas de crear. `JOIN` busca el producto interno de cada oferta. Usamos **proveedor y referencia** porque cada proveedor define sus propios códigos. Completa los dos huecos del bloque.

```sql
WITH ofertas AS (
  SELECT 'A' AS supplier_id, supplier_sku, product_name, price_eur, available_units
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_a`
  UNION ALL
  SELECT supplier_id, supplier_sku, product_name, price_eur, available_units
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur`
  -- Completa con el operador que añade las filas del proveedor C.
  SELECT 'C', article_ref, label, CAST(unit_price_eur AS NUMERIC), units_on_hand
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_c`
)
SELECT
  p.product_id,
  p.product_name AS producto,
  p.sales_unit AS unidad,
  o.supplier_id AS proveedor,
  o.price_eur AS precio_eur,
  o.available_units AS stock,
  o.available_units >= 50 AS cubre_50
FROM ofertas AS o
JOIN `TU_PROJECT_ID.terra_taronja_biglake.lab03_correspondencias` AS m
  -- Completa el JOIN. Sustituye FALSE por la comparación entre las referencias de o y m.
JOIN `TU_PROJECT_ID.terra_taronja_biglake.lab03_productos` AS p
  ON m.product_id = p.product_id
ORDER BY producto, cubre_50 DESC, precio_eur, stock DESC, proveedor;
```

Espera **48 ofertas de 20 productos**. Las tres ofertas de Naranja de Carcaixent deben tener el mismo `product_id` (**1**) y la unidad **bolsa de 1 kg**. `cubre_50` indica si el stock alcanza para el pedido. Las ofertas que lo pueden cubrir salen primero dentro de cada producto y se ordenan por precio.

## 5. Recomienda una compra · 5 min

Necesitamos **50 bolsas de Naranja de Carcaixent** y **50 tarros de Alcachofa en conserva de Benicarló**. Elige un proveedor para cada producto. Justifica ambas elecciones con el precio y las unidades disponibles. ¿Cambiarías la decisión si pidieras solo **20 tarros**?

<details>
<summary>Compara tu respuesta con los datos</summary>

- **Naranja.** A ofrece 128 bolsas a **3,65 €** y C ofrece 210 a **4,05 €**. B tiene el precio más bajo, **3,20 €**, y está agotado. Para 50 bolsas, A cubre el pedido al menor precio.
- **Alcachofa.** Para 50 tarros, C es el único que llega, con 107 a **5,45 €**. Para 20, B sale más barato, con 23 a **4,14 €**. A tiene 30 a **4,69 €**.

</details>

<details>
<summary>Opcional · Comprueba la puntualidad de las entregas</summary>

Una entrega está a tiempo cuando llegó en la fecha prevista o antes. Completa el cálculo del porcentaje por proveedor.

```sql
SELECT
  supplier_id AS proveedor,
  COUNT(*) AS entregas,
  COUNTIF(delivered_date <= expected_date) AS a_tiempo,
  -- Completa el porcentaje usando los cálculos de las dos columnas anteriores.
  -- Redondea el resultado a un decimal.
  NULL AS porcentaje
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_entregas`
GROUP BY proveedor
ORDER BY proveedor;
```

Espera **16 de 24 (66,7 %)** para A, **18 de 24 (75,0 %)** para B y **22 de 24 (91,7 %)** para C. Es un indicador del proveedor en este histórico. ¿Pagarías más por un proveedor que suele llegar a tiempo si el pedido tiene una fecha límite?

</details>

## Último paso · Limpieza completa del entorno

**9 minutos.** Retira los recursos de los tres laboratorios para dejar de almacenar archivos de clase y evitar que sigan usándose por error. Trabaja solo en tu proyecto de la práctica. **Conserva el proyecto de GCP y cualquier recurso ajeno a BigLake.**

**Primero, borra la vista del Lab 03 y las tablas externas que pudiste crear a mano en los Labs 01 y 02.** En **BigQuery Studio → SQL query**, sustituye `TU_PROJECT_ID` por tu proyecto, revisa los nombres y pulsa **Run**.

```sql
DROP VIEW IF EXISTS `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur`;
DROP EXTERNAL TABLE IF EXISTS `TU_PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`;
DROP EXTERNAL TABLE IF EXISTS `TU_PROJECT_ID.terra_taronja_biglake_a01.proveedor_b_biglake`;
```

Terraform retirará las seis tablas externas `lab03_...` y los archivos de origen durante el borrado de los tres labs. [Borrado de vistas](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_view_statement) · [Borrado de tablas externas](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_external_table_statement)

### Ejecuta los tres destroy en orden

Vuelve a la terminal que usaste para desplegar el Lab 03. Ejecuta un comando de borrado cada vez y espera a que termine antes de continuar. Cada `terraform destroy` muestra qué quiere borrar. Comprueba tu proyecto, la lista de recursos del lab indicado y escribe `yes` cuando estés conforme.

1. **Lab 03**. Abre PowerShell en `bigLake/lab03/terraform` dentro de `SQL`. Borra primero las seis tablas que leen archivos y usan recursos de los otros dos labs. Su plan también lee las salidas de esos estados.

   ```powershell
   terraform destroy
   ```

2. **Lab 02**. Desde la carpeta de Terraform del Lab 03, cambia a la del Lab 02.

   ```powershell
   cd ../../lab02/terraform
   ```

   <details>
   <summary>Si tu bucket del Lab 02 aún tiene borrado recuperable de 7 días</summary>

   Compruébalo en **Cloud Storage → Buckets → tu bucket del Lab 02 → Protection**. Desde la carpeta del Lab 02, ejecuta `terraform plan`. Si solo cambia la retención a `0` y retira del estado las dos entradas duplicadas de las APIs de BigQuery y Cloud Storage, ejecuta `terraform apply` y confirma con `yes`. Las APIs siguen habilitadas. Espera al menos 30 segundos tras el cambio antes de borrar el bucket. Los objetos que ya estaban en borrado recuperable conservan su plazo original. [Cómo se aplica el cambio de política](https://docs.cloud.google.com/storage/docs/disable-soft-delete)

   </details>

   Una vez en `bigLake/lab02/terraform`, copia la plantilla que desactiva temporalmente los bloqueos de borrado. Terraform retirará la conexión, la cuenta de prueba y sus permisos, el dataset de B y el bucket restringido.

   ```powershell
   Copy-Item -LiteralPath 'cleanup_override.tf.example' -Destination 'cleanup_override.tf'
   terraform destroy
   ```

   Cuando termine correctamente o si cancelas el borrado, quita la copia temporal para volver a activar los bloqueos.

   ```powershell
   Remove-Item -LiteralPath 'cleanup_override.tf'
   ```

3. **Lab 01**. Desde la carpeta de Terraform del Lab 02, cambia a la del Lab 01.

   ```powershell
   cd ../../terraform
   ```

   Una vez en `bigLake/terraform`, borra el dataset, los seis objetos del bucket original y el propio bucket.

   ```powershell
   terraform destroy
   ```

### Comprueba el resultado

- En **BigQuery Studio → Explorer**, actualiza la página. Deben desaparecer `terra_taronja_biglake`, `terra_taronja_biglake_a01` y la conexión `terra_taronja_restringida`.
- En **Cloud Storage → Buckets**, comprueba que ya no aparecen `TU_PROJECT_ID-terra-taronja-biglake` y `TU_PROJECT_ID-terra-taronja-biglake-lab02`. Si personalizaste el nombre del segundo bucket, comprueba ese nombre.
- En **IAM & Admin → Service Accounts**, comprueba que desapareció `biglake-lab02-analyst`. Terraform retiró la concesión de lectura que la conexión tenía en el bucket restringido.
- Si quieres comprobar los estados, ejecuta `terraform state list` en cada una de las tres carpetas. No deben quedar recursos gestionados por Terraform. Las APIs siguen habilitadas en el proyecto para que otros recursos puedan utilizarlas.

Si el borrado falla, corrige la causa y repite el comando del lab que falló antes de seguir.

- **El dataset contiene tablas.** Comprueba el SQL inicial y el borrado del Lab 03. Si creaste otra tabla manualmente para la práctica, revisa su nombre y bórrala en BigQuery Studio. Si te interesa conservar una tabla, guárdala en otro dataset antes de reintentar.
- **El bucket contiene archivos adicionales.** Mueve los que quieras conservar a otro bucket antes de reintentar.
- **Aparece `prevent_destroy` en el Lab 02.** Comprueba que copiaste `cleanup_override.tf` en la carpeta de ese Terraform.
