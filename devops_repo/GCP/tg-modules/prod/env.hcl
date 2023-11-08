locals {
  global_env          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env                 = "prod"
  gcp_project_id      = "fastapi-387914"
  gcp_project_name    = "FastAPI"
  gcp_sa_prefix       = "fastapi"
  gke_version_channel = "STABLE"
  gke_version_prefix  = "1.27.3"
  
  gcp_sa_roles  = [
    "${local.gcp_project_id}=>roles/viewer",
    "${local.gcp_project_id}=>roles/storage.admin",
    "${local.gcp_project_id}=>roles/storage.objectViewer",
    "${local.gcp_project_id}=>roles/compute.networkAdmin",
    "${local.gcp_project_id}=>roles/compute.securityAdmin",
    "${local.gcp_project_id}=>roles/compute.storageAdmin",
    "${local.gcp_project_id}=>roles/compute.osAdminLogin",
    "${local.gcp_project_id}=>roles/compute.serviceAgent",
    "${local.gcp_project_id}=>roles/container.serviceAgent",
    "${local.gcp_project_id}=>roles/container.clusterAdmin",
    "${local.gcp_project_id}=>roles/container.admin",
    "${local.gcp_project_id}=>roles/secretmanager.admin",
    "${local.gcp_project_id}=>roles/file.editor",
    "${local.gcp_project_id}=>roles/cloudkms.admin",
    "${local.gcp_project_id}=>roles/cloudsql.admin",
    "${local.gcp_project_id}=>roles/monitoring.metricWriter",
    "${local.gcp_project_id}=>roles/monitoring.viewer",
    "${local.gcp_project_id}=>roles/logging.logWriter",
    "${local.gcp_project_id}=>roles/logging.configWriter",
  ]
  gcp_api_services  = [
    "cloudkms.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "container.googleapis.com",
    "servicenetworking.googleapis.com",
    "dns.googleapis.com",
    "networkmanagement.googleapis.com",
    "cloudapis.googleapis.com",
    "firestore.googleapis.com",
    "file.googleapis.com",
    "iam.googleapis.com",
    "iap.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "secretmanager.googleapis.com",
    "servicemanagement.googleapis.com",
    "serviceusage.googleapis.com",
    "sql-component.googleapis.com",
    "sqladmin.googleapis.com",
    "stackdriver.googleapis.com",
    "storage-component.googleapis.com",
    "storage.googleapis.com",
  ]

}
