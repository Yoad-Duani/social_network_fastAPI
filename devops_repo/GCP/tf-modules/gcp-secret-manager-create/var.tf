variable "secrets_id" {
  description = "list of secrets from gcp"
  type = set(string)
}

variable "project_id" {
  description = "GCP project ID"
}

variable "env_name" {
  description = "GCP env"
}