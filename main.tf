terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
  }
}


provider "google" {
  credentials = file(var.creds)
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "reddit-bucket" {
  name          = var.google_storage_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "redit-bq" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.location
  delete_contents_on_destroy = true
}


resource "google_bigquery_dataset" "bq_dev" {
  dataset_id                 = var.bq_dev
  location                   = var.location
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "bq_prod" {
  dataset_id                 = var.bq_prod
  location                   = var.location
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "bq_dbt" {
  dataset_id                 = var.bq_dbt
  location                   = var.location
  delete_contents_on_destroy = true
}