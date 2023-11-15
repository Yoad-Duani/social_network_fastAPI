//dependencies {
//  paths = ["${get_terragrunt_dir()}/../gcp-subnets"]
//}

dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-project-services"]
}



locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                        = local.env_vars.locals.global_env.locals

  env_name                          = local.env_vars.locals.env
  base_source_url                   = local.env_global.base_source_url
  base_source_module                = local.env_global.base_source_module
  base_source_provider              = local.env_global.base_source_provider
  gcp_project_id                    = local.env_vars.locals.gcp_project_id
  gcp_region                        = local.env_global.gcp_region
  gcp_default_zone                  = local.env_global.gcp_default_zone
}

inputs = {
  gcp_project_id        = local.gcp_project_id
  gcp_region            = local.gcp_region
  gcp_default_zone      = local.gcp_default_zone
  gke_version_channel   = local.env_vars.locals.gke_version_channel
  gke_version_prefix    = local.env_vars.locals.gke_version_prefix
  env                   = local.env_name
}