variable "secrets_id" {
  description = "list of secrets from gcp"
  type = list(string)
}

variable "project_id" {
  description = "GCP project ID"
}

variable "env_name" {
  description = "GCP env"
}