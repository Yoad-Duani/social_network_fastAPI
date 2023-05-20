locals {
  env                       = "prod"
  cloud                     = "GCP"
  gcp_region                = ""
  gcp_region_zones          = ["",""]
  gcp_project_id            = ""
  gcp_project_name          = ""
  gcp_vpc_name              = ""
  gcp_gce_kms_master_key    = "" 

  // General settings

  base_source_url                   = "git::https://github.com/Yoad-Duani/social_network_fastAPI/devops_repo/tf-modules.git"
  base_source_provider              = "GCP"
  base_source_kubernetes_provider   = "Kubernete"
  base_source_helm_provider         = "Helm"
  base_source_ref                   = "main"
  
  google_tf_source_url              = "git::https://github.com/terraform-google-modules/terraform-google-vm"
  google_tf_source_provider         = "modules"
  google_tf_source_module           = "instance_template"
  google_tf_source_ref              = "7.9.0"
}