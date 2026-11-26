output "location" {
  description = "Ubicación común del bucket, la conexión y los datasets."
  value       = local.location
}

output "connection" {
  description = "ID completo de la conexión para GoogleSQL y BigQuery Studio."
  value       = "${var.project_id}.${lower(google_bigquery_connection.restricted.location)}.${google_bigquery_connection.restricted.connection_id}"
}

output "connection_service_account" {
  description = "Cuenta de servicio creada y gestionada por BigQuery para la conexión."
  value       = google_bigquery_connection.restricted.cloud_resource[0].service_account_id
}

output "proveedor_b_uri" {
  description = "Ruta del objeto restringido para crear la tabla BigLake."
  value       = local.proveedor_b_uri
}

output "analyst_service_account" {
  description = "Correo de la cuenta restringida que se impersona desde Cloud Shell."
  value       = google_service_account.analyst.email
}

output "dataset_id" {
  description = "Dataset de BigQuery para crear la tabla del proveedor B."
  value       = google_bigquery_dataset.catalogue.dataset_id
}
