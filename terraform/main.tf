terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "d0_raw_landing" {
  name     = "${var.project_id}-d0-raw-landing"
  location = var.region

  uniform_bucket_level_access = true

  public_access_prevention = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }

    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id = "d1_staged_enforced"
  location   = var.region

  description = "D1 Staged/Enforced dataset for validated onboarding data."

  delete_contents_on_destroy = false

  default_table_expiration_ms = 2592000000
}

resource "google_service_account" "pipeline" {
  account_id   = "habot-pipeline"
  display_name = "Habot Data Pipeline Service Account"
  description  = "Least-privilege service account for the Habot data pipeline."
}

resource "google_storage_bucket_iam_member" "d0_raw_landing_viewer" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.pipeline.email}"

  condition {
    title       = "RawLandingReadAccess"
    description = "Allow the pipeline to read objects from the raw landing bucket."
    expression  = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.d0_raw_landing.name}/objects/')"
  }
}

resource "google_bigquery_table" "student_onboarding" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_onboarding"

  deletion_protection = true

  schema = <<EOF
[
  {
    "name": "student_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "student_name",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "email",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "country",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "organization_id",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_bigquery_row_access_policy" "organization_filter" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id
  policy_id  = "organization_filter"

  filter_predicate = "organization_id = 'habot'"

  grantees = [
    "serviceAccount:${google_service_account.pipeline.email}"
  ]
}

resource "google_bigquery_dataset_iam_member" "pipeline_data_editor" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.pipeline.email}"
}
