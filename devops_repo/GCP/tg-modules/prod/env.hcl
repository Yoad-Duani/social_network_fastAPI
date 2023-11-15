locals {
  global_env            = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env                   = "prod"
  gcp_project_id        = "fastapi-387914"
  gcp_project_name      = "fastapi"
  gcp_sa_prefix         = "fastapi"

  
  // GKE Prod env
  gke_version_channel                 = "STABLE"
  gke_version_prefix                  = "1.27.3"
  gke_ip_range_pods                   = "${local.global_env.locals.gcp_node_subnet_name}-${local.gcp_project_id}-${local.env}-pods"
  gke_ip_range_services               = "${local.global_env.locals.gcp_node_subnet_name}-${local.gcp_project_id}-${local.env}-svcs"
  gke_http_load_balancing             = false
  gke_network_policy                  = true
  gke_horizontal_pod_autoscaling      = true
  gke_filestore_csi_driver            = false
  gke_enable_private_endpoint         = true
  gke_enable_private_nodes            = true
  gke_regional                        = true
  gke_logging_enabled_components      = ["SYSTEM_COMPONENTS"]
  gke_ip_masq_link_local              = true
  gke_configure_ip_masq               = false

  gke_default_max_pods_per_node       = 32
  gke_create_service_account          = false
  gke_remove_default_node_pool        = true
  gke_enable_shielded_nodes           = true
  gke_initial_node_count              = 0
  gke_machine_type                    = "e2-standard-4"
  gke_gce_pd_csi_driver               = true
  gke_deploy_using_private_endpoint   = true




  gke_master_authorized_networks  = [
    {
      master_ipv4_cidr_block      = "${local.global_env.locals.gcp_node_subnet_cidr}"
      display_name                = "${local.gcp_project_id}-network-shared-ic-1-subnet-${local.env}"
    }
  ]





  
  
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
