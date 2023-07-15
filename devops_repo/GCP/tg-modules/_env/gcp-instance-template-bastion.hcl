
###
dependency "gcp-vpc" {
  config_path = "/mnt/c/yoad-new/study/python/fastAPI/devops_repo/GCP/tg-modules/prod/gcp-vpc"
}

dependency "gcp-subnets" {
    config_path = "/mnt/c/yoad-new/study/python/fastAPI/devops_repo/GCP/tg-modules/prod/gcp-subnets"
}
###


locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                      = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                    = local.env_vars.locals.global_env.locals

  account_vars                  = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  org                           = local.account_vars.locals.org
  env_name                      = local.env_vars.locals.env

  gcp_project_id                = local.env_vars.locals.gcp_project_id
  gcp_project_name              = local.env_vars.locals.gcp_project_name
  gcp_default_zone              = local.env_global.gcp_default_zone
  gcp_region                    = local.env_global.gcp_region
  gcp_subnet_name               = "${local.env_global.gcp_node_subnet_name}-${local.env_name}-general"
  gcp_network_project_id        = local.env_global.gcp_network_project_id
  gcp_bastion_image_project_id  = local.env_global.gcp_bastion_image_project_id
  gcp_bastion_source_image      = local.env_global.gcp_bastion_source_image
  gcp_bastion_macine_type       = local.global_env.gcp_bastion_macine_type
  gcp_node_sa                   =
  gcp_enable_shielded_vm        =
  gcp_shielded_instance_config  =

  service_account   = {
    email = 
    scopes = 
  }

}