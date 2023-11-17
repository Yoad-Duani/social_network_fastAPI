variable "gcp_region" {
  description = "The GCP region to deploy to (e.g us-east-1)"
}

variable "gcp_project_id" {
  description = "The GCP project ID"
}

variable "env" {
  description = "The environment, e.g prod, dev, stage"
}

variable "tags" {
  description   = "extra tags"
  type          = map
  default       = {}
}