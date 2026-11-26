variable "project_id" {
  description = "ID del proyecto GCP individual del alumno."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Introduce el ID del proyecto GCP (6 a 30 caracteres), tal como aparece en la consola."
  }
}

variable "region" {
  description = "Región de Cloud SQL permitida en el proyecto del alumno."
  type        = string
  default     = "europe-west1"
  nullable    = false
}
