output "bucket_name" {
  description = "Nombre del bucket privado con los archivos de la clase."
  value       = google_storage_bucket.terra_taronja.name
}

output "dataset_id" {
  description = "Dataset de prácticas en BigQuery, incluido el proyecto."
  value       = "${var.project_id}.${google_bigquery_dataset.terra_taronja.dataset_id}"
}

output "proveedor_a_uri" {
  description = "URI que se pega al crear la tabla externa del Lab 01."
  value       = "gs://${google_storage_bucket.terra_taronja.name}/${google_storage_bucket_object.source["proveedor_a.csv"].name}"
}
