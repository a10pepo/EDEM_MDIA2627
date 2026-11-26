resource "google_sql_database_instance" "terra_taronja" {
  name             = "terra-taronja-lab1"
  database_version = "POSTGRES_16"
  region           = var.region

  # El laboratorio es desechable. Habilita el borrado desde Terraform.
  deletion_protection = false

  settings {
    edition                     = "ENTERPRISE"
    tier                        = "db-f1-micro"
    availability_type           = "ZONAL"
    disk_type                   = "PD_HDD"
    disk_size                   = 10
    disk_autoresize             = false
    deletion_protection_enabled = false
    retain_backups_on_delete    = false
    data_api_access             = "ALLOW_DATA_API"

    ip_configuration {
      # Studio usa la consola de Google Cloud. La lista de redes autorizadas queda vacía.
      ipv4_enabled = true
      ssl_mode     = "ENCRYPTED_ONLY"
    }

    backup_configuration {
      enabled                        = false
      point_in_time_recovery_enabled = false
    }

    final_backup_config {
      enabled = false
    }
  }
}

resource "google_sql_database" "terra_taronja" {
  name     = "terra_taronja"
  instance = google_sql_database_instance.terra_taronja.name
}
