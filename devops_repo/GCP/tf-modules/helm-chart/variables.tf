
variable "gke_name" {}
variable "gke_endpoint" {}
variable "gke_ca_cert" {}

variable "namespace" {
  default = "default"
}

variable "enabled" {
  default = 1
}

variable "values_file_path" {
  default = "values.yaml"
}

variable "name" {}
variable "chart" {}
variable "repository" {}
variable "chart_version" {}

