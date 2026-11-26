# BigLake · Lab 02 · Consulta un catálogo con acceso delegado

**30 minutos · Trabajo individual · BigQuery Studio**

Terra Taronja vende productos de la Comunitat Valenciana. El proveedor B envía su catálogo en **NDJSON**, con un objeto JSON por línea. Quiere que el equipo de compras pueda consultar precios y existencias en BigQuery, y que el archivo original en Cloud Storage siga protegido.

En Cloud Storage, un **bucket** es un contenedor donde se guardan archivos. BigQuery leerá el catálogo desde el bucket privado de este lab. La tabla que vas a crear se guarda en un **dataset**, que es el espacio donde BigQuery agrupa tablas.

Crearás la tabla BigLake con tu usuario habitual, que es **Owner** de tu proyecto. Luego usarás una cuenta de servicio de prueba para intentar leer el archivo directamente y para consultar la tabla. La misma cuenta de prueba recibirá dos respuestas distintas.

## Despliega Terraform del Lab 02

**5 minutos.** Terraform crea el bucket privado del Lab 02, sube el archivo del proveedor B y prepara la conexión, el dataset y la cuenta de prueba. Ejecuta Terraform con tu usuario **Owner** en el proyecto donde ya desplegaste el Lab 01, que habilita las APIs de BigQuery y Cloud Storage. El nombre del bucket se genera a partir de tu Project ID. Mantén la ubicación **EU** para el Lab 03.

1. Si ya configuraste las credenciales de Terraform en el Lab 01 con tu usuario Owner, puedes reutilizarlas. Si es la primera vez con esa cuenta, ejecuta `gcloud auth login` y luego los comandos siguientes. Sustituye `TU_PROJECT_ID` por tu **Project ID** y autoriza Terraform con tu cuenta habitual.

   ```text
   gcloud config set project TU_PROJECT_ID
   gcloud auth application-default login
   ```

2. Abre PowerShell en la carpeta `SQL`, que contiene `bigLake`, y ejecuta estos comandos. Si ya existe `terraform.tfvars` en la carpeta del Lab 02, ejecuta solo la primera línea.

   ```powershell
   cd bigLake/lab02/terraform
   Copy-Item terraform.tfvars.example terraform.tfvars
   ```

   Abre `terraform.tfvars` en esa carpeta. Escribe el mismo `project_id` que usaste en el Lab 01 y, en `owner_email`, el correo que ves arriba a la derecha en la consola cuando entras con tu usuario **Owner**. Terraform concederá a ese correo permiso para impersonar la cuenta de prueba. Si vienes de una versión anterior del Lab 02, añade `owner_email` a tu archivo y elimina el bloque `student_emails` si sigue ahí.

   ```hcl
   project_id  = "TU_PROJECT_ID"
   owner_email = "TU_CORREO_OWNER"
   ```

3. Ejecuta `init` y revisa con `plan` lo que se va a crear. Comprueba el proyecto y los recursos del Lab 02. Después ejecuta `apply` y escribe `yes` cuando te pida confirmación.

   ```text
   terraform init
   terraform plan
   terraform apply
   ```

   En el primer despliegue, Terraform espera a que IAM reconozca las cuentas de servicio. Si aparece `Service account … does not exist`, espera un minuto y vuelve a ejecutar `terraform apply` en la misma carpeta para completar los pasos pendientes.

4. Comprueba la dirección del archivo y el correo de la cuenta de prueba. Los usarás en la actividad.

   ```text
   terraform output -raw proveedor_b_uri
   terraform output -raw analyst_service_account
   ```

5. Abre [BigQuery Studio](https://console.cloud.google.com/bigquery) con tu usuario habitual, en tu proyecto. En **Explorer**, comprueba que aparece `terra_taronja_biglake_a01`.

## 1. Localiza el archivo del proveedor B · 2 min

En **Explorer → Datasets**, abre `terra_taronja_biglake_a01` y entra en **Details**. Copia la dirección de **Description**. Empieza por `gs://` y termina en `/clase03/proveedor_b.ndjson`. La pegarás en los pasos 3 y 5. [Consultar los detalles de un dataset](https://docs.cloud.google.com/bigquery/docs/listing-datasets)

Tu usuario Owner puede leer el archivo porque tiene permisos en su proyecto. En el Lab 01, la tabla externa convencional se apoyaba en ese acceso. Ahora queremos que una cuenta con permisos de BigQuery pueda consultar el catálogo sin tener acceso directo al archivo.

## 2. Explora la conexión · 2 min

1. En **Explorer**, abre tu proyecto y entra en **Connections**.
2. Selecciona `terra_taronja_restringida`. Comprueba su **Location** y localiza el **Service account ID** en los detalles.
3. La conexión tiene su propia cuenta de servicio. BigQuery la usa para leer el archivo del bucket. En el paso 5 usarás otra cuenta, `biglake-lab02-analyst`, para hacer las pruebas. [Consultar los detalles de una conexión](https://docs.cloud.google.com/bigquery/docs/working-with-connections)

## 3. Crea la tabla BigLake · 6 min

1. En **Explorer → Datasets**, vuelve al dataset que abriste en el paso 1. Anota su nombre completo, incluido el sufijo. En **Actions**, pulsa **Create table**.
2. En **Create table from**, elige **Google Cloud Storage**. Pega la dirección original que empieza por `gs://` en **Select file from GCS bucket or use a URI pattern**. Si el campo ya muestra `gs://` o rechaza el nombre del bucket al pegar la URI, pega la parte que empieza por el nombre del bucket. El acceso para **Browse** requiere permisos adicionales sobre Cloud Storage. En **File format**, elige **JSONL (Newline delimited JSON)**.
3. En **Destination**, selecciona tu proyecto y el dataset `terra_taronja_biglake_a01`. Escribe `proveedor_b_biglake` en **Table** y selecciona **External table** en **Table type**.
4. Marca **Create a BigLake table using a Cloud Resource connection**. En **Connection ID**, selecciona la conexión `terra_taronja_restringida` en la ubicación indicada.
5. En **Schema**, deja **Auto-detect** desmarcado, activa **Edit as text** y pega el siguiente esquema. Pulsa **Create table**. [Crear una tabla BigLake en la consola](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake)

```json
[
  {"name": "product_code", "type": "STRING"},
  {"name": "description", "type": "STRING"},
  {"name": "price_cents", "type": "INTEGER"},
  {"name": "stock", "type": "INTEGER"}
]
```

Abre la tabla y revisa **Schema** y **Details**. Comprueba que aparecen las cuatro columnas y que la URI de origen coincide con la descripción del dataset.

<details>
<summary>Si el formulario no acepta la ruta o la conexión, crea la tabla desde SQL</summary>

Abre [03_crear_tabla_biglake.sql](./solucion/03_crear_tabla_biglake.sql) y copia el código en **SQL query**. Sustituye `TU_PROJECT_ID` por el ID de tu proyecto, `UBICACION` por la ubicación de la conexión en minúsculas y `URI_NDJSON` por la dirección completa de **Description**. Ejecuta el bloque con **Run**. [CREATE EXTERNAL TABLE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_table_statement)

</details>

## 4. Consulta el catálogo · 4 min

En el [archivo de ejemplo](../datos/proveedor_b.ndjson), `product_code` es la referencia del proveedor, `description` identifica el producto y su presentación, `price_cents` guarda el precio en céntimos y `stock` indica las unidades disponibles.

Pulsa **SQL query**. Abre el archivo SQL de cada pregunta, copia su contenido y sustituye `TU_PROJECT_ID` por el ID de tu proyecto. Ejecuta una consulta cada vez con **Run**.

**¿Cuántas ofertas tiene el proveedor B y cuántas tienen stock?**

El resultado es **16 ofertas y 14 con stock**. [Consulta de recuento](./solucion/04_1_recuento.sql)

**¿Cuáles son los tres productos disponibles más baratos?**

El precio de la tabla se obtiene al dividir los céntimos entre 100. [Consulta de las tres ofertas](./solucion/04_2_ofertas_mas_baratas.sql)

| Referencia | Producto | Precio por unidad comercial | Stock |
| --- | --- | ---: | ---: |
| B-0170 | Zumo de naranja de Carcaixent | 2,15 € | 102 |
| B-0163 | Garrofón de Cullera | 2,81 € | 76 |
| B-0114 | Zumo de granada de Elche | 2,98 € | 58 |

## 5. Valida el acceso delegado desde Cloud Shell · 11 min

**Impersonar una cuenta de servicio** significa pedirle a Google una credencial temporal para ejecutar un comando con los permisos de esa cuenta. Harás las dos pruebas como `biglake-lab02-analyst`.

### Abre Cloud Shell y prepara los valores

1. En la barra superior de la consola de Google Cloud, pulsa **Activate Cloud Shell** (icono `>_`). Se abrirá una terminal Bash en la parte inferior. Si aparece **Authorize**, pulsa ese botón para que Cloud Shell pueda usar tu cuenta. Ejecuta estas dos líneas para comprobar el proyecto y el usuario que inicia los comandos. Si aparece otro correo, abre Cloud Shell desde la consola con el usuario Owner que desplegó Terraform. [Abrir Cloud Shell](https://docs.cloud.google.com/shell/docs/using-cloud-shell)

   ```bash
   gcloud config get-value project
   gcloud auth list --filter='status:ACTIVE' --format='value(account)'
   ```

2. Pega esta línea. Cuando se muestre la pregunta, pega el mismo **Project ID** que escribiste en `terraform.tfvars` y pulsa Enter. Los comandos de la prueba usarán este valor, incluso si la terminal tenía seleccionado otro proyecto.

   ```bash
   read -r -p 'Project ID del Lab 02: ' LAB02_PROJECT
   ```

3. Copia las líneas siguientes. El correo mostrado debe coincidir con `terraform output -raw analyst_service_account`. Puedes encontrar la misma cuenta en **IAM & Admin → Service Accounts**, con el nombre **Terra Taronja · Analista del Lab 02**. Si usaste una ubicación distinta, sustituye `EU` por el valor de **Location** del paso 2.

   ```bash
   LAB02_ANALYST="biglake-lab02-analyst@${LAB02_PROJECT}.iam.gserviceaccount.com"
   LAB02_LOCATION='EU'
   printf 'Cuenta de prueba: %s\n' "$LAB02_ANALYST"
   ```

4. Pega esta línea. Cuando se muestre la pregunta, pega la dirección del paso 1, con `gs://` al principio, y pulsa Enter. Usa la ruta del bucket restringido del Lab 02.

   ```bash
   read -r -p 'Dirección gs:// del NDJSON: ' LAB02_URI
   ```

### Prueba A · Lee el archivo directamente

Pega el bloque completo. El argumento `--impersonate-service-account` indica a `gcloud` que use la cuenta de prueba en este comando. Anota el correo que muestra `gcloud` al anunciar la impersonación y el resultado. [Impersonación en un comando de gcloud](https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation)

```bash
gcloud storage cat "$LAB02_URI" \
  --project="$LAB02_PROJECT" \
  --impersonate-service-account="$LAB02_ANALYST"
```

El resultado esperado es **403** o **PERMISSION_DENIED** por falta de `storage.objects.get`. Eso comprueba el permiso efectivo sobre ese archivo. Si el mensaje menciona `iam.serviceAccounts.getAccessToken`, la prueba se detuvo antes de llegar a Cloud Storage. Comprueba la cuenta activa y la concesión de **Service Account Token Creator** de la cuenta de prueba.

### Prueba B · Consulta la tabla BigLake

Pega el bloque completo. La primera línea indica a `bq` qué cuenta debe impersonar durante esta ejecución. El cambio dura lo que dura ese comando. [Impersonación en bq](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference#use_a_service_account) · [Variable de impersonación de Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/authenticate)

```bash
CLOUDSDK_AUTH_IMPERSONATE_SERVICE_ACCOUNT="$LAB02_ANALYST" \
  bq --project_id="$LAB02_PROJECT" --location="$LAB02_LOCATION" \
  query --use_legacy_sql=false \
  "SELECT SESSION_USER() AS mi_cuenta, COUNT(*) AS ofertas
   FROM \`${LAB02_PROJECT}.terra_taronja_biglake_a01.proveedor_b_biglake\`"
```

Comprueba que `mi_cuenta` muestra `biglake-lab02-analyst@…iam.gserviceaccount.com`, el mismo correo de la prueba A, y que `ofertas` devuelve **16**. Si aparece tu correo personal, revisa que pegaste el bloque entero, incluida la primera línea. Si la tabla no se encuentra, comprueba que la creaste en el paso 3 y revisa `LAB02_PROJECT` y `LAB02_LOCATION`. [Identidad devuelta por SESSION_USER](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/security_functions#session_user)

Puedes consultar el SQL de esta prueba por separado. Para comprobar el acceso delegado, ejecuta el bloque de Cloud Shell de arriba con la identidad de analista. [SQL de la prueba B](./solucion/05_identidad_y_ofertas.sql)

**Conclusión.** La cuenta de prueba recibió **403** al pedir el archivo. La misma cuenta obtuvo **16 ofertas** al consultar BigQuery. En esa consulta, BigQuery leyó el archivo usando la cuenta de servicio de la conexión.

<details>
<summary>Comprueba los permisos si el resultado es distinto</summary>

Terraform da **BigQuery Job User** en tu proyecto y **BigQuery Data Viewer** en el dataset a la cuenta de prueba. La cuenta de servicio de la conexión tiene **Storage Object Viewer** en el bucket. Tu usuario Owner recibe **Service Account Token Creator** sobre la cuenta de prueba. [Permisos para consultar BigLake](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake) · [Permisos para impersonar](https://docs.cloud.google.com/iam/docs/service-account-permissions)

El plan simulado valida las concesiones declaradas y las pruebas locales verifican la sintaxis. La propagación de IAM, los permisos heredados y las respuestas **403** y **16 ofertas** se comprueban al ejecutar las pruebas A y B en tu proyecto.

Si en la prueba A aparecen las filas, revisa **IAM & Admin → IAM** y **Cloud Storage → Buckets → tu bucket del Lab 02 → Permissions**. Busca el correo de la cuenta de prueba y revisa las concesiones directas y las heredadas del proyecto, carpeta u organización. Cualquier concesión efectiva de `storage.objects.get` sobre el archivo invalida la prueba de aislamiento. [Herencia en Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam)

También puedes comprobar que la cuenta de prueba no puede hacerse pasar por la cuenta de la conexión. Pega esta línea y, cuando aparezca la pregunta, pega el **Service account ID** de la conexión que viste en el paso 2.

```bash
read -r -p 'Correo de la cuenta de servicio de la conexión: ' LAB02_CONNECTION_SA
```

Pega el siguiente bloque. Pide la credencial a través de la cuenta de prueba y descarta la salida del comando. Se espera un error de permisos al intentar pasar de la cuenta de prueba a la cuenta de la conexión. [Impersonación con una cadena de cuentas](https://docs.cloud.google.com/sdk/gcloud/reference#--impersonate-service-account)

```bash
gcloud auth print-access-token --project="$LAB02_PROJECT" \
  --impersonate-service-account="$LAB02_ANALYST,$LAB02_CONNECTION_SA" > /dev/null
```

</details>

### Termina la prueba

Los comandos A y B aplicaron la impersonación solo a esas ejecuciones. Tu sesión de Google Cloud y el proyecto activo se conservan. Limpia las variables del lab y comprueba que sigue apareciendo tu usuario habitual.

```bash
unset LAB02_PROJECT LAB02_ANALYST LAB02_LOCATION LAB02_URI LAB02_CONNECTION_SA
gcloud auth list --filter='status:ACTIVE' --format='value(account)'
```

**Para comentar.** ¿Qué identidad leyó el archivo durante el `SELECT`? ¿Qué permiso está usando Cloud Storage para evaluar la descarga directa? ¿En qué se diferencia del acceso del Lab 01?

### Limpieza al terminar la clase

Conserva el bucket, el archivo y la conexión para el Lab 03. Cuando termines la clase, sigue la [limpieza completa del Lab 03](../lab03/README.md#último-paso--limpieza-completa-del-entorno). Incluye el borrado de `proveedor_b_biglake` y el orden para retirar la infraestructura de los tres labs.
