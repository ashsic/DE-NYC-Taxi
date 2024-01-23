variable "credentials" {
  description = "GCP credentials"
  default     = "./keys/my-first-key.json"
}


variable "project" {
  description = "Project"
  default     = "bustling-surge-411418"
}

variable "location" {
  description = "Location of GCP Resources"
  default     = "US"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "test_dataset"
}

variable "gsb_bucket_name" {
  description = "My Google Storage Bucket Name"
  default     = "ashsic-terraform-test-bucket1234"
}

variable "gsb_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}