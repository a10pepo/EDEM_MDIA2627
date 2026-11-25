locals {
  location = "EU"
  source_files = toset([
    "deliveries.csv",
    "product_supplier_map.csv",
    "products.csv",
    "proveedor_a.csv",
    "proveedor_b.ndjson",
    "proveedor_c.parquet",
  ])
}

resource "google_project_service" "lab" {
  for_each = toset(["bigquery.googleapis.com", "storage.googleapis.com"])

  service            = each.value
  disable_on_destroy = false
}

resource "google_bigquery_dataset" "terra_taronja" {
  dataset_id                 = "terra_taronja_biglake"
  location                   = local.location
  delete_contents_on_destroy = false

  depends_on = [google_project_service.lab["bigquery.googleapis.com"]]
}

resource "google_storage_bucket" "terra_taronja" {
  name                        = "${var.project_id}-terra-taronja-biglake"
  location                    = local.location
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  # Los datos de clase son sintéticos y se pueden volver a subir desde el repositorio.
  soft_delete_policy {
    retention_duration_seconds = 0
  }

  depends_on = [google_project_service.lab["storage.googleapis.com"]]
}

resource "google_storage_bucket_object" "source" {
  for_each = local.source_files

  bucket = google_storage_bucket.terra_taronja.name
  name   = "clase03/${each.value}"
  source = "${path.module}/../datos/${each.value}"
}
