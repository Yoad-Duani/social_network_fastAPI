
variable "gcp_region" {
  description = "The GCP region to deploy"
}

variable "gcp_project_id" {
  description = "The GCP project ID"
}

variable "org" {
  description = "The organiztion name"
}

variable "env" {
  description = "Environment like prod, dev"
}

variable "extra_tags" {
  description = "Extra tags to attach"
  type = map
  default = {}
}
