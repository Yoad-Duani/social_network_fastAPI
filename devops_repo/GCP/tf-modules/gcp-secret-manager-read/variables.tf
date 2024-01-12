variable "secrets" {
  description = "list of secrets from gcp"
  type = set(string)
}

variable "project_id" {
  description = "GCP project ID"
}
