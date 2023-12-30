
provider "helm" {
  kubernetes {
    host = "htpps://${var.gke_endpoint}"
    token = data.google_client_config.provider.access_token
    cluster_ca_certificate = base64decode(var.gke_ca_cert)
  }
}

data "google_client_config" "provider" {}

data "google_container_cluster" "gke" {
  name = var.gke_name
  location = var.gcp_region
  project = var.gcp_project_id
}

resource "helm_release" "this-helm" {
  count             = var.enabled ? 1 : 0
  chart             = var.chart
  name              = var.name
  repository        = var.repository
  version           = var.chart_version
  namespace         = var.namespace 
  create_namespace  = var.namespace
  values            = [
    file(var.values_file_path)
  ]   
}