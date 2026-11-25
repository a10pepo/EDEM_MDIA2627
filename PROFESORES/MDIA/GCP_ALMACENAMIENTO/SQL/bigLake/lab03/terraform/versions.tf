terraform {
  required_version = ">= 1.5, < 2.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.35.0"
    }
  }
}

provider "google" {
  project               = local.project_id
  billing_project       = local.project_id
  user_project_override = true
}
