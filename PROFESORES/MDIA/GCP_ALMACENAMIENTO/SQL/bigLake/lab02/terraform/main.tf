locals {
  location        = contains(["EU", "US"], upper(var.location)) ? upper(var.location) : lower(var.location)
  proveedor_b_uri = "gs://${google_storage_bucket.restricted.name}/${google_storage_bucket_object.proveedor_b.name}"
}

resource "google_project_service" "lab" {
  # BigQuery y Cloud Storage se habilitan en el Lab 01.
  for_each = toset([
    "bigqueryconnection.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}

resource "google_storage_bucket" "restricted" {
  name                        = coalesce(var.bucket_name, "${var.project_id}-terra-taronja-biglake-lab02")
  location                    = local.location
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  soft_delete_policy {
    retention_duration_seconds = 0
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_storage_bucket_object" "proveedor_b" {
  bucket       = google_storage_bucket.restricted.name
  name         = "clase03/proveedor_b.ndjson"
  source       = "${path.module}/../../datos/proveedor_b.ndjson"
  content_type = "application/x-ndjson"

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_bigquery_connection" "restricted" {
  connection_id = "terra_taronja_restringida"
  friendly_name = "Terra Taronja · Catálogo restringido"
  location      = local.location

  cloud_resource {}

  lifecycle {
    prevent_destroy = true
  }

  depends_on = [
    google_project_service.lab["bigqueryconnection.googleapis.com"],
    google_project_service.lab["cloudresourcemanager.googleapis.com"],
  ]
}

moved {
  from = google_bigquery_dataset.student["a01"]
  to   = google_bigquery_dataset.catalogue
}

resource "google_bigquery_dataset" "catalogue" {
  dataset_id                 = "terra_taronja_biglake_a01"
  description                = local.proveedor_b_uri
  location                   = local.location
  delete_contents_on_destroy = false
}
