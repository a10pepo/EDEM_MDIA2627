variable "project_id" {
  description = "ID del proyecto propio del alumno con facturación vinculada."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Introduce el ID del proyecto GCP (6 a 30 caracteres)."
  }
}

variable "owner_email" {
  description = "Correo del usuario Owner que ejecutará las pruebas de Cloud Shell."
  type        = string
  nullable    = false

  validation {
    condition = (
      can(regex("^[^@\\s:]+@[^@\\s:]+\\.[^@\\s:]+$", var.owner_email)) &&
      !endswith(lower(var.owner_email), ".gserviceaccount.com")
    )
    error_message = "Introduce el correo de tu usuario Owner, sin el prefijo user:."
  }
}

variable "location" {
  description = "Ubicación común del bucket, la conexión y los datasets. Usa EU para continuar con la ubicación del Lab 01."
  type        = string
  default     = "EU"
  nullable    = false

  validation {
    condition     = contains(["EU", "US"], upper(var.location)) || can(regex("^[a-z]+(-[a-z0-9]+)+[0-9]$", lower(var.location)))
    error_message = "Indica EU, US o una región común a BigQuery y Cloud Storage, como europe-west1."
  }
}

variable "bucket_name" {
  description = "Nombre opcional del bucket. Si se omite, Terraform lo genera a partir del ID del proyecto."
  type        = string
  default     = null

  validation {
    condition     = var.bucket_name == null || can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "Usa entre 3 y 63 letras minúsculas, números o guiones, con letra o número al principio y al final."
  }
}
