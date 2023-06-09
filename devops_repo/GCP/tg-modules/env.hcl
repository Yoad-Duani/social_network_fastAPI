locals {
#  env                              = "prod"
  cloud                             = "GCP"
  gcp_region                        = "us-central1"
  gcp_region_zones                  = ["us-central-a"]
# gcp_project_id                    = "fastapi-387914"
# gcp_project_name                  = "FastAPI"
  gcp_vpc_name                      = "my-vpc"
  gcp_gce_kms_master_key            = "fastapi-kms-master-key" 

  ## General settings

  base_source_url                   = "git::https://github.com/Yoad-Duani/social_network_fastAPI/devops_repo/tf-modules.git"
  base_source_provider              = "GCP"
  base_source_kubernetes_provider   = "Kubernete"
  base_source_helm_provider         = "Helm"
  base_source_ref                   = "main"
  
  google_tf_source_url              = "git::https://github.com/terraform-google-modules"
  google_tf_source_provider         = "modules"
  google_tf_source_module           = "instance_template"
  google_tf_source_ref              = "7.9.0"


  gcp_sa_prefix                     = "fastapi"
  gcp_sa_names                      = ["project-sa", "terraform-sa"]
  gcp_sa_description                = "Managed by Terraform" 

  test_env                          = "test env 11111111"
}