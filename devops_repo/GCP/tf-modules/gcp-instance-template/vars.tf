

variable "gcp_region" {
  description = "The GCP region to deploy to (e.g us-east-1)"
}

variable "gcp_project_id" {
  description = "The GCP project ID"
}

variable "org" {
  description = "The organization"
}

variable "env" {
  description = "The environment, e.g prod, dev, stage"
}

variable "extra_tags" {
  description = "Extra tags to attach to things"
  type        = map
  default     = {}
}