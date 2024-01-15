dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts"]
}

dependency "gcp-vpc" {
  config_path = "${get_terragrunt_dir()}/../gcp-vpc"
  mock_outputs_allowed_terraform_commands = ["validate", "init", "plan"]
  mock_outputs = {
    network_name = "fake-name"
  }
  mock_outputs_merge_strategy_with_state = "shallow"
}

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                            = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                          = local.env_vars.locals.global_env.locals

  google_tf_source_url                = local.env_global.google_tf_source_url
  google_tf_source_provider           = local.env_global.google_tf_source_provider
  google_tf_source_module             = "terraform-google-sql-db"

  env_name                            = local.env_vars.locals.env
  gcp_project_id                      = local.env_vars.locals.gcp_project_id
  gcp_project_name                    = local.env_vars.locals.gcp_project_name
  gcp_region                          = local.env_global.gcp_region

  gcp_private_service_access_ip             = local.env_global.gcp_allocated_ip_range_private_service_access
  gcp_private_service_access_prefix_length  = local.env_global.gcp_allocated_prefix_length_private_service_access
  gcp_private_service_access_ip_version     = local.env_global.gcp_private_service_access_ip_version
}

inputs = {
  project_id          = local.gcp_project_id
  address             = local.gcp_private_service_access_ip
  ip_version          = local.gcp_private_service_access_ip_version
  prefix_length       = local.gcp_private_service_access_prefix_length
  vpc_network         = dependency.gcp-vpc.outputs.network_name
}