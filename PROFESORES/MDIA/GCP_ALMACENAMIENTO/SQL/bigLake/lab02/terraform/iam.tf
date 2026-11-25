resource "time_sleep" "connection_identity" {
  # La cuenta de servicio que crea BigQuery puede tardar en estar disponible en IAM.
  create_duration = "90s"

  triggers = {
    service_account = google_bigquery_connection.restricted.cloud_resource[0].service_account_id
  }
}

resource "google_storage_bucket_iam_member" "connection_reader" {
  bucket = google_storage_bucket.restricted.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${time_sleep.connection_identity.triggers["service_account"]}"
}

resource "google_service_account" "analyst" {
  account_id   = "biglake-lab02-analyst"
  display_name = "Terra Taronja · Analista del Lab 02"

  depends_on = [google_project_service.lab["iam.googleapis.com"]]
}

resource "time_sleep" "analyst_identity" {
  # IAM necesita tiempo para reconocer la cuenta al asignar sus roles.
  create_duration = "90s"

  triggers = {
    email = google_service_account.analyst.email
  }
}

resource "google_service_account_iam_member" "owner_token_creator" {
  service_account_id = google_service_account.analyst.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "user:${var.owner_email}"

  depends_on = [time_sleep.analyst_identity]
}

resource "google_project_iam_member" "analyst_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${time_sleep.analyst_identity.triggers["email"]}"
}

resource "google_bigquery_dataset_iam_member" "analyst_data_viewer" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.catalogue.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${time_sleep.analyst_identity.triggers["email"]}"
}
