locals {
#  env                              = "prod"
  cloud                             = "GCP"
  gcp_region                        = "me-west1"
# gcp_region_zones                  = ["me-west1-a", "me-west1-b"]
  gcp_region_zones                  = ["me-west1-a"]
  gcp_default_zone                  = "a"
# gcp_project_id                    = "fastapi-387914"
# gcp_project_name                  = "FastAPI"
  gcp_vpc_name                      = "vpc"
  gcp_gce_kms_master_key            = "fastapi-kms-master-key" 

  ## General settings

  base_source_url                   = "git::https://github.com/Yoad-Duani"
  base_source_module                = "social_network_fastAPI"
  base_source_provider              = "devops_repo/GCP/tf-modules"
  base_source_kubernetes_provider   = "Kubernete"
  base_source_helm_provider         = "Helm"
  base_source_ref                   = "main"
  
  google_tf_source_url              = "git::https://github.com/terraform-google-modules"
  google_tf_source_provider         = "modules"
  #google_tf_source_module           = "instance_template"
  #google_tf_source_ref              = "7.9.0"


  //gcp_sa_prefix                     = "fastapi"
  gcp_sa_names                      = ["project-sa", "terraform-sa"]
  gcp_sa_description                = "Managed by Terraform" 

  test_env                          = "test env 11111111111"

  gcp_node_subnet_name              = "subnet"
  gcp_node_subnet_description       = "general purpose"
  gcp_node_subnet_cidr              = "172.20.10.0/24"

  // GKE Global env
  gke_node_subnet_name              = "subnet"
  gke_node_subnet_description       = "GKE subnet purpose"
  gke_node_subnet_cidr              = "172.20.11.0/24"
  gke_master_ipv4_cidr_block        = "172.20.20.0/28"
  gke_logging_service               = "logging.googleapis.com/kubernetes"
  gke_ip_range_pods                 = "172.21.0.0/16"
  gke_ip_range_services             = "172.22.0.0/16"


  gcp_network_project_id            = "fastapi-387914"
  gcp_bastion_image_project_id      = "ubuntu-os-cloud"
  gcp_bastion_source_image          = "ubuntu-2204-jammy-v20230630"
  gcp_bastion_macine_type           = "e2-small"
}