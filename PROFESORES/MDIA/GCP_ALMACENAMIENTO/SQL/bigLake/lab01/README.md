# BigLake · Lab 01 · Consulta el catálogo de un proveedor

**25 minutos · Trabajo individual · BigQuery Studio**

Después de analizar las ventas y el abastecimiento, Terra Taronja decidió incorporar nuevos proveedores. Los tres ofrecen alimentos de la Comunitat Valenciana y envían sus catálogos en formatos distintos. Hoy abrirás el **CSV del proveedor A** desde BigQuery para averiguar qué productos podrías comprar y cuáles están disponibles.

Crearás una **tabla externa convencional**. BigQuery guardará el esquema y la dirección del archivo, y leerá el CSV de Cloud Storage al ejecutar una consulta.

## Antes de empezar

- Ten a mano el **Project ID** de tu propio proyecto de Google Cloud con facturación vinculada. Usa la misma cuenta de clase en la terminal y en la consola.
- Descarga el repositorio completo y ábrelo en tu terminal. Necesitas Terraform 1.5 o posterior y Google Cloud CLI. Los seis archivos de clase ya están en [`datos/`](../datos/).
- Usa tu cuenta **Owner** en el proyecto de la práctica. Si cuentas con roles separados, el despliegue y las consultas requieren **Service Usage Admin**, **Storage Admin** y **BigQuery User** en ese proyecto. [Permisos de Service Usage](https://docs.cloud.google.com/service-usage/docs/access-control) · [Roles de Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam-roles) · [Permisos de tablas externas](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage#required_roles)

## 1. Prepara tu entorno con Terraform · 5 min

Terraform crea el dataset `terra_taronja_biglake` y un bucket privado en **EU**. También sube los seis archivos a `clase03/`. En este laboratorio usarás [`proveedor_a.csv`](../datos/proveedor_a.csv), que tiene una fila por oferta. Los otros archivos quedan preparados para la clase.

1. Si es la primera vez que usas Google Cloud CLI con tu cuenta de clase, ejecuta `gcloud auth login`. Después selecciona tu proyecto y obtén las credenciales de aplicación que lee Terraform. Sustituye `TU_PROJECT_ID` por tu ID real. Si ya configuraste esas credenciales en el lab de Cloud SQL con la misma cuenta, puedes reutilizarlas. [Autenticación de Terraform en Google Cloud](https://docs.cloud.google.com/docs/terraform/authentication)

   ```text
   gcloud config set project TU_PROJECT_ID
   gcloud auth application-default login
   ```

2. Abre PowerShell en la carpeta `SQL`, que contiene `bigLake`, y entra en [`bigLake/terraform`](../terraform/). Copia el archivo de ejemplo con el siguiente comando. Abre `terraform.tfvars` y pon tu **Project ID** en `project_id`.

   ```powershell
   cd bigLake/terraform
   Copy-Item terraform.tfvars.example terraform.tfvars
   ```

3. Descarga el proveedor con `init` y revisa con `plan` lo que se va a crear. Comprueba el proyecto, el dataset, el bucket y los seis objetos. Si coincide con tu proyecto, ejecuta `apply` y escribe `yes` cuando te pida confirmación.

   ```text
   terraform init
   terraform plan
   terraform apply
   ```

   <details>
   <summary>Si falla el plan o ya creaste el dataset a mano</summary>

   Si el error indica que **Service Usage API** está deshabilitada, sustituye `TU_PROJECT_ID` por el ID de tu proyecto y ejecuta `gcloud services enable serviceusage.googleapis.com --project=TU_PROJECT_ID`. Vuelve a ejecutar `terraform plan`.

   Si ya creaste en **EU** el dataset dedicado a esta práctica, puedes incorporarlo al estado de Terraform. Ejecuta el siguiente comando después de `terraform init`, con el ID de tu proyecto, y revisa el plan antes de aplicarlo. Terraform gestionará también su borrado al terminar la clase. [Importación de datasets](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset#import)

   ```text
   terraform import google_bigquery_dataset.terra_taronja projects/TU_PROJECT_ID/datasets/terra_taronja_biglake
   ```

   </details>

4. Copia la URI que devuelve este comando. Tendrá la forma `gs://TU_PROJECT_ID-terra-taronja-biglake/clase03/proveedor_a.csv`.

   ```text
   terraform output -raw proveedor_a_uri
   ```

5. En [Cloud Storage → Buckets](https://console.cloud.google.com/storage/browser), abre tu bucket y comprueba que en **Objects** aparecen los seis archivos bajo `clase03/`. En [BigQuery Studio](https://console.cloud.google.com/bigquery), abre **Explorer** y localiza `terra_taronja_biglake` dentro de tu proyecto. Si acabas de desplegarlo, actualiza la página. [Ubicación de las tablas externas](https://docs.cloud.google.com/bigquery/docs/external-tables#location_considerations)

## 2. Crea la tabla externa · 7 min

En BigQuery Studio, abre `terra_taronja_biglake` y pulsa **Create table**.

1. En **Create table from**, elige **Google Cloud Storage**. Usa **Browse** y selecciona `clase03/proveedor_a.csv` dentro de tu bucket. Si prefieres pegar la URI en **Select file from GCS bucket or use a URI pattern** y el campo muestra `gs://` o rechaza el nombre del bucket, pega solo la parte que empieza en el nombre del bucket, como `tu-project-id-terra-taronja-biglake/clase03/proveedor_a.csv`. En **File format**, elige **CSV**.
2. En **Destination**, elige tu proyecto y `terra_taronja_biglake`. Escribe `proveedor_a_ext` en **Table** y elige **External table** en **Table type**.
3. En **Schema**, deja **Auto-detect** desmarcado. Activa **Edit as text** y pega el esquema de debajo.
4. Antes de pulsar **Create table**, abre **Advanced options**. Pon **1** en **Header rows to skip** y deja la coma como delimitador. La primera línea contiene los nombres de las columnas. Si queda en **0**, BigQuery intentará leer el texto `price_eur` como un precio decimal. [Crear una tabla externa desde Cloud Storage](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage) · [Opciones de CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#csv_options)

```json
[
  {"name": "supplier_sku", "type": "STRING"},
  {"name": "product_name", "type": "STRING"},
  {"name": "price_eur", "type": "NUMERIC"},
  {"name": "available_units", "type": "INTEGER"}
]
```

En **Schema**, comprueba que el precio es decimal y las unidades son enteras. En **Details**, localiza la URI del archivo que lee la tabla. El proveedor usa `supplier_sku` como referencia propia. El precio está en euros por unidad comercial y el stock indica cuántas de esas unidades están disponibles.

## 3. Comprueba los datos con SQL · 8 min

Pulsa **SQL query**. Sustituye `PROJECT_ID` por el ID de tu proyecto en cada consulta y ejecuta los bloques por separado con **Run**.

**Mira las primeras cinco filas por referencia.**

```sql
SELECT supplier_sku, product_name, price_eur, available_units
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`
ORDER BY supplier_sku
LIMIT 5;
```

Con los datos de clase, la primera fila es **A-0107 · Naranja de Carcaixent**, a **3,65 €**, con **128 unidades**.

**Comprueba cuántas ofertas se leen del CSV.**

```sql
SELECT COUNT(*) AS ofertas
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`;
```

El resultado esperado es **16 ofertas**.

- Si aparece `CSV processing encountered too many errors` con **17 filas y 1 error**, comprueba si el detalle menciona la primera fila o la columna `price_eur`. Si se leyó la cabecera como un dato, elimina únicamente la tabla externa `proveedor_a_ext` en **More → Delete** y vuelve al paso 2 con **Header rows to skip** en **1**. El CSV permanece en Cloud Storage. [Errores de lectura de CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#troubleshooting)
- Si aparece **Access Denied**, comprueba que la URI apunta a tu bucket y que estás usando la misma cuenta que en Terraform.
- Si indica que el recurso no está disponible en esa ubicación, comprueba **EU** en **Edit → Query settings** y la ubicación del dataset.

**Localiza las referencias agotadas.**

```sql
SELECT supplier_sku, product_name
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`
WHERE available_units = 0
ORDER BY supplier_sku;
```

Deberías encontrar **2 referencias sin stock**. Una referencia puede seguir en el catálogo aunque en ese momento tenga cero unidades.

## 4. Reto y reflexión · 5 min

Queremos comprar **50 unidades** de un producto que cueste como máximo **4 € por unidad**. Escribe una consulta que devuelva las **tres referencias con más stock** que cumplan ambas condiciones. Si empatan en stock, ordénalas por `supplier_sku`. ¿Cuál presentarías primero al equipo de compras?

- ¿En qué recurso está el CSV y qué guardaste al crear la tabla externa?
- Si el proveedor actualiza un precio, ¿en qué sitio hay que cambiar el dato?
- ¿Qué información adicional pedirías antes de hacer un pedido al proveedor?

Puedes contrastar tus respuestas con las [soluciones del Lab 01](./solucion/). Sustituye `PROJECT_ID` por el ID de tu proyecto antes de ejecutar cualquiera de esos archivos.

## Limpieza al terminar la clase

Conserva el bucket, los seis archivos, el dataset y la carpeta de trabajo de Terraform para los siguientes laboratorios. Al terminar la clase, sigue la [limpieza completa del Lab 03](../lab03/README.md#último-paso--limpieza-completa-del-entorno). Allí borrarás la tabla externa que creaste a mano y ejecutarás los tres `terraform destroy` en orden. El almacenamiento y las consultas pueden generar cargos. [Costes de las tablas externas](https://docs.cloud.google.com/bigquery/docs/external-tables#pricing)
