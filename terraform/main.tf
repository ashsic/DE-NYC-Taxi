terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  project = "bustling-surge-411418"
  region  = "us-central1"
}

resource "google_storage_bucket" "test-bucket" {
  name          = "ashsic-terraform-test-bucket1234"
  location      = "US"
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