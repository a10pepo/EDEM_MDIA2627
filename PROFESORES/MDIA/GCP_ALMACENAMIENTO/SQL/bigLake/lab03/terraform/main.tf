data "terraform_remote_state" "lab01" {
  backend = "local"
  config = {
    path = "${path.module}/../../terraform/terraform.tfstate"
  }
}

data "terraform_remote_state" "lab02" {
  backend = "local"
  config = {
    path = "${path.module}/../../lab02/terraform/terraform.tfstate"
  }
}

locals {
  lab01 = data.terraform_remote_state.lab01.outputs
  lab02 = data.terraform_remote_state.lab02.outputs

  project_id = split(".", local.lab01.dataset_id)[0]
  dataset_id = split(".", local.lab01.dataset_id)[1]
  source_dir = "gs://${local.lab01.bucket_name}/clase03"

  # El orden de las columnas coincide con el de cada CSV.
  csv_sources = {
    lab03_proveedor_a = {
      uri = local.lab01.proveedor_a_uri
      columns = [
        ["supplier_sku", "STRING"],
        ["product_name", "STRING"],
        ["price_eur", "NUMERIC"],
        ["available_units", "INTEGER"],
      ]
    }
    lab03_productos = {
      uri = "${local.source_dir}/products.csv"
      columns = [
        ["product_id", "INTEGER"],
        ["product_name", "STRING"],
        ["category", "STRING"],
        ["origin_region", "STRING"],
        ["origin_province", "STRING"],
        ["origin_locality", "STRING"],
        ["list_price_cents", "INTEGER"],
        ["catalog_since", "DATE"],
        ["sales_unit", "STRING"],
      ]
    }
    lab03_correspondencias = {
      uri = "${local.source_dir}/product_supplier_map.csv"
      columns = [
        ["supplier_id", "STRING"],
        ["supplier_sku", "STRING"],
        ["product_id", "INTEGER"],
      ]
    }
    lab03_entregas = {
      uri = "${local.source_dir}/deliveries.csv"
      columns = [
        ["delivery_id", "STRING"],
        ["supplier_id", "STRING"],
        ["supplier_sku", "STRING"],
        ["ordered_date", "DATE"],
        ["expected_date", "DATE"],
        ["delivered_date", "DATE"],
        ["ordered_units", "INTEGER"],
        ["received_units", "INTEGER"],
      ]
    }
  }
}

resource "google_bigquery_table" "csv" {
  for_each = local.csv_sources

  dataset_id          = local.dataset_id
  table_id            = each.key
  deletion_protection = false

  external_data_configuration {
    autodetect    = false
    source_format = "CSV"
    source_uris   = [each.value.uri]
    schema        = jsonencode([for column in each.value.columns : { name = column[0], type = column[1] }])

    csv_options {
      quote             = "\""
      skip_leading_rows = 1
    }
  }
}

resource "google_bigquery_table" "proveedor_b" {
  dataset_id          = local.dataset_id
  table_id            = "lab03_proveedor_b"
  deletion_protection = false
  schema = jsonencode([
    { name = "product_code", type = "STRING" },
    { name = "description", type = "STRING" },
    { name = "price_cents", type = "INTEGER" },
    { name = "stock", type = "INTEGER" },
  ])

  external_data_configuration {
    autodetect    = false
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = [local.lab02.proveedor_b_uri]
    connection_id = local.lab02.connection
  }

  lifecycle {
    precondition {
      condition     = split(".", local.lab02.connection)[0] == local.project_id && upper(local.lab02.location) == "EU"
      error_message = "Los Labs 01 y 02 deben estar desplegados en el mismo proyecto y en EU para reutilizar su dataset y conexión."
    }
  }
}

resource "google_bigquery_table" "proveedor_c" {
  dataset_id          = local.dataset_id
  table_id            = "lab03_proveedor_c"
  deletion_protection = false

  external_data_configuration {
    # Parquet guarda su esquema en el propio archivo.
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = ["${local.source_dir}/proveedor_c.parquet"]
  }
}
