
data "google_container_engine_versions" "channel" {
  provider       = google-beta
  location       = "${var.gcp_region}-${var.gcp_default_zone}"
  project        = var.gcp_project_id
  version_prefix = "1.27."
}

data "google_compute_zones" "available" {
    project = var.gcp_project_id
    region = var.gcp_region
}