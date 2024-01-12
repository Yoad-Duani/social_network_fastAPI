dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts", "${get_terragrunt_dir()}/../gcp-secrets-create"]
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

  # google_tf_source_url              = local.env_global.google_tf_source_url
  # google_tf_source_provider         = local.env_global.google_tf_source_provider
  # google_tf_source_module           = ""
  base_source_url                     = local.env_global.base_source_url
  base_source_module                  = local.env_global.base_source_module
  base_source_provider                = local.env_global.base_source_provider

  env_name                            = local.env_vars.locals.env
  gcp_project_id                      = local.env_vars.locals.gcp_project_id
  gcp_project_name                    = local.env_vars.locals.gcp_project_name

  read_secrets_postgresql             = local.env_global.read_secrets_postgresql
  # read_secrets_mysql                = local.env_global.read_secrets_mysql
  
}


inputs = {
  secrets         = local.read_secrets_postgresql
  # secrets       = local.read_secrets_mysql
  project_id      = local.gcp_project_id
}