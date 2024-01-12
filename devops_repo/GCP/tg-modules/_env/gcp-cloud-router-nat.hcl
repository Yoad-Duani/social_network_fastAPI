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
  google_tf_source_module             = "terraform-google-cloud-router"

  env_name                            = local.env_vars.locals.env
  gcp_project_id                      = local.env_vars.locals.gcp_project_id
  gcp_project_name                    = local.env_vars.locals.gcp_project_name
  gcp_region                          = local.env_global.gcp_region

  
}


inputs = {
  project    = local.gcp_project_id
  network       = dependency.gcp-vpc.outputs.network_name
  name          = "${dependency.gcp-vpc.outputs.network_name}-${local.env_name}-router"
  region        = local.gcp_region
  nats          = [
    {
      name        = "${dependency.gcp-vpc.outputs.network_name}-${local.env_name}-nat"
      log_config  = {
        enable    = true
        filter    = "ERRORS_ONLY"
      }  
    }
  ]
}