# Lab 1 · Cloud SQL con Terraform

Despliega una instancia de PostgreSQL 16 y la base de datos `terra_taronja` en tu proyecto de GCP. Comprueba el acceso con una consulta de lectura en Cloud SQL Studio. La base queda vacía y se reutilizará en un laboratorio posterior.

## 1. Prepara tu proyecto

1. Abre la [consola de Google Cloud](https://console.cloud.google.com/). Selecciona el proyecto individual que te han asignado o créalo siguiendo las indicaciones del profesor.
2. Copia el **ID del proyecto** desde el selector. En los comandos de esta guía, sustituye `PROJECT_ID` por ese ID. El ID es el que aparece en `terraform.tfvars`, `gcloud` y el plan de Terraform.
3. En **Facturación**, comprueba que el proyecto está vinculado a una cuenta activa. La instancia genera cargos desde que se aprovisiona. El borrado está previsto para el Lab 4. [Precios de Cloud SQL](https://cloud.google.com/sql/pricing)
4. Para desplegar y completar todo el lab, necesitas **Cloud SQL Admin** (`roles/cloudsql.admin`) y el permiso `serviceusage.services.use` en tu proyecto. Si te faltan, comparte el apartado [Acceso al proyecto](#acceso-al-proyecto) con el administrador.

## 2. Autentica la terminal

Necesitas Terraform 1.5 o posterior de la serie 1.x y la CLI de Google Cloud. En una terminal local, instala ambas herramientas. Si usas Cloud Shell, guarda tu copia del repositorio en el directorio personal para conservar el estado entre sesiones. `gcloud` viene instalado y Terraform se instala por separado. Comprueba las herramientas con `terraform version` y `gcloud version`. [Instalar Terraform](https://developer.hashicorp.com/terraform/install) · [Instalar gcloud](https://docs.cloud.google.com/sdk/docs/install) · [Instalar Terraform en Cloud Shell](https://docs.cloud.google.com/docs/terraform/install-configure-terraform#cloud-shell)

**Terminal local.** En el navegador, elige la misma cuenta de Google que usas en la consola para este proyecto. El primer inicio de sesión es para `gcloud`. El segundo crea las credenciales predeterminadas de aplicación (ADC) que utiliza Terraform. [Autenticación de Terraform en Google Cloud](https://docs.cloud.google.com/docs/terraform/authentication)

```sh
gcloud auth login
gcloud config set project PROJECT_ID
gcloud auth application-default login
gcloud auth application-default set-quota-project PROJECT_ID
```

**Cloud Shell.** Usa las credenciales de la sesión de la consola. Selecciona el proyecto y acepta la autorización de Cloud Shell si aparece. [Autenticación en Google Cloud](https://docs.cloud.google.com/docs/terraform/authentication)

```sh
gcloud config set project PROJECT_ID
```

Comprueba la cuenta activa y el proyecto.

```sh
gcloud auth list
gcloud config get-value project
```

En **APIs y servicios**, comprueba si **Cloud SQL Admin API** (`sqladmin.googleapis.com`) ya está habilitada. Si falta y tienes el permiso `serviceusage.services.enable`, ejecuta el comando siguiente. Si te falta el permiso, pide al administrador que habilite la API antes de seguir. [Habilitar servicios de Google Cloud](https://docs.cloud.google.com/service-usage/docs/enable-disable)

```sh
gcloud services enable sqladmin.googleapis.com --project=PROJECT_ID
```

## 3. Configura Terraform

Abre una terminal en la carpeta `SQL`, donde están `cloudSQL`, `bigQuery` y `bigLake`. Entra en el directorio del lab.

```sh
cd cloudSQL/lab01
```

En Cloud Shell, macOS o Linux, ejecuta `cp terraform.tfvars.example terraform.tfvars`. En PowerShell, ejecuta `Copy-Item terraform.tfvars.example terraform.tfvars`.

Abre `terraform.tfvars` y sustituye el valor de `project_id` por el ID de tu proyecto. Conserva `europe-west1` (Bélgica) o indica la región que haya autorizado el profesor. Guarda aquí solo el ID y la región. Conserva esta carpeta de trabajo hasta el Lab 4. Terraform guarda aquí el estado local que vincula el código con tus recursos.

## 4. Inicializa, revisa y despliega

```sh
terraform init
terraform validate
terraform plan '-out=lab1.tfplan'
```

`init` instala el proveedor de Google. `validate` comprueba la configuración. `plan` muestra lo que Terraform haría y guarda el resultado para aplicarlo después. Conserva las comillas alrededor de `-out=lab1.tfplan` para que PowerShell lo pase como un único argumento.

En un primer despliegue, espera `Plan: 2 to add, 0 to change, 0 to destroy`. Comprueba el ID del proyecto en `terraform.tfvars`. En el plan, revisa la región, la instancia `terra-taronja-lab1` y la base `terra_taronja`. La instancia debe ser Enterprise, con tipo `db-f1-micro`, disponibilidad `ZONAL` y disco HDD de 10 GB. Si cambias la configuración, genera y revisa un plan nuevo.

Cuando hayas revisado el plan y tengas autorización para generar cargos en ese proyecto, ejecuta el plan guardado. Este comando aplica directamente el plan revisado.

```sh
terraform apply lab1.tfplan
```

Espera a que el comando termine. En la consola, selecciona tu proyecto y abre **Cloud SQL → Instancias → terra-taronja-lab1**. En **Descripción general**, verifica que está operativa, en la región esperada y con PostgreSQL 16. En **Bases de datos**, busca `terra_taronja`. También verás bases que PostgreSQL y Cloud SQL crean por defecto.

## 5. Configura la contraseña de PostgreSQL

1. Abre la pestaña **Usuarios** de la instancia. Localiza el usuario integrado `postgres`.
2. En su menú **⋮**, elige **Cambiar contraseña**. Genera una contraseña larga y única con tu gestor de contraseñas y pégala en el formulario. Guarda el cambio y espera a que finalice.
3. Conserva la contraseña solo en tu gestor. Mantenla fuera de Git, de `terraform.tfvars`, de scripts y de capturas. Terraform no recibe la contraseña, por lo que tampoco la escribe en el plan ni en el estado. [Cambiar la contraseña del usuario predeterminado](https://docs.cloud.google.com/sql/docs/postgres/create-manage-users#set-password)

## 6. Comprueba la conexión en Cloud SQL Studio

1. En el menú de la misma instancia, abre **Cloud SQL Studio**.
2. Selecciona `terra_taronja`, el método de **autenticación integrada de la base de datos** y el usuario `postgres`. Introduce la contraseña en el formulario e inicia sesión.
3. Ejecuta esta consulta. El resultado esperado es una fila con `terra_taronja` y `postgres`. [Usar Cloud SQL Studio](https://docs.cloud.google.com/sql/docs/postgres/manage-data-using-studio)

```sql
SELECT current_database() AS base_de_datos, current_user AS usuario;
```

4. Comprueba que el esquema `public` está vacío. Esta consulta debe devolver cero filas.

```sql
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';
```

La instancia tiene una IPv4 pública asignada, con conexiones directas bloqueadas al mantener vacía la lista de redes autorizadas. Studio se abre desde la consola con permisos de Google Cloud y credenciales de PostgreSQL. Comprueba la lista en **Conexiones → Redes** y déjala vacía. [Redes autorizadas de Cloud SQL](https://docs.cloud.google.com/sql/docs/postgres/authorize-networks)

| Si ocurre esto | Comprueba esto |
| --- | --- |
| Studio muestra `403` o un error de permiso | Confirma la cuenta y el proyecto de la consola y que la cuenta tenga `cloudsql.instances.executeSql`. |
| PostgreSQL rechaza la contraseña | Selecciona la autenticación integrada, `postgres` y `terra_taronja`. Repite el cambio de contraseña en **Usuarios** si hace falta. |
| La conexión se agota o la base no aparece | Comprueba en **Descripción general** que la instancia está operativa y que la base existe. En **Conexiones → Redes**, verifica que **Permitir API de datos** está activado. Recarga la página cuando terminen las operaciones pendientes. |
| Un cliente directo a la IPv4 falla | Usa Studio para esta práctica. Mantén vacía la lista de redes autorizadas. |

## 7. Conserva la instancia para reutilizarla

Cierra la sesión de Studio y deja en funcionamiento `terra-taronja-lab1`. En el Lab 2 usarás esa misma instancia y la base `terra_taronja` en tu proyecto. Conserva `terraform.tfvars` y el estado local `terraform.tfstate` en la carpeta del Lab 1. [Guía del Lab 2](../lab02/README.md)

**El borrado se hará en el Lab 4** con `terraform destroy`, desde esta misma carpeta. Cloud SQL sigue generando cargos mientras la instancia esté aprovisionada. Para estimar el coste de la práctica, usa las tarifas de tu región para la instancia `db-f1-micro` y los 10 GiB de disco HDD durante las horas que esté aprovisionada. [Cierre del bloque](../lab04/README.md#cierre-del-curso) · [Precios de Cloud SQL](https://cloud.google.com/sql/pricing)

## Acceso al proyecto

| Tarea | Rol o permiso |
| --- | --- |
| Desplegar y borrar la instancia, cambiar la contraseña y usar Studio | **Cloud SQL Admin** (`roles/cloudsql.admin`) en el proyecto individual. |
| Usar el proyecto como proyecto de cuota de ADC | `serviceusage.services.use`. Si hace falta, el administrador puede conceder **Service Usage Consumer** (`roles/serviceusage.serviceUsageConsumer`). |
| Habilitar **Cloud SQL Admin API** | `serviceusage.services.enable`. El administrador puede habilitarla antes de la práctica. |
| Usar solo Studio con una base preparada | **Cloud SQL Studio User** (`roles/cloudsql.studioUser`) y credenciales de PostgreSQL. Si la cuenta no puede listar instancias, pide al administrador el enlace directo o acceso a la lista. |

Google Cloud comprueba los permisos de la cuenta con la que abres Studio. PostgreSQL comprueba por separado el usuario y la contraseña que introduces al conectarte. [Roles de Cloud SQL](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudsql) · [Roles de Service Usage](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage)

## Si Terraform falla

| Síntoma | Qué revisar |
| --- | --- |
| `terraform init` no descarga el proveedor | Comprueba la conectividad con Terraform Registry y las descargas de HashiCorp. Si la red local bloquea el acceso, prueba en Cloud Shell. |
| Faltan credenciales predeterminadas o se usa otra cuenta | En local, revisa el inicio de sesión ADC y si `GOOGLE_APPLICATION_CREDENTIALS` apunta a otras credenciales. En Cloud Shell, confirma la cuenta de la consola y acepta la autorización de la sesión. |
| `USER_PROJECT_DENIED` o `SERVICE_DISABLED` | Revisa el proyecto de cuota, el permiso `serviceusage.services.use`, la API y la facturación. |
| La máquina no está disponible o aparece un error de cuota o política de red | Comprueba que la región admita `db-f1-micro` en Enterprise y que tu proyecto tenga cuota y permita IPv4 pública para Cloud SQL. |
| `apply` se interrumpe o la instancia ya existe (`409`) | Revisa las operaciones de Cloud SQL y ejecuta `terraform state list`. Si hay una operación en curso, espera a que termine y vuelve a generar el plan. Si la instancia existe y no aparece en el estado, comprueba con el administrador su proyecto y su origen antes de tocarla. |
