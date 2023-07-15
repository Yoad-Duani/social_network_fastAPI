
locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                  = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                = local.env_vars.locals.global_env.locals

  google_tf_source_url      = local.env_global.google_tf_source_url
  google_tf_source_provider = local.env_global.google_tf_source_provider
  google_tf_source_module   = "terraform-google-project-factory"

  project_id                =   local.env_vars.locals.gcp_project_id
  activate_apis             =   local.env_vars.locals.gcp_api_services
}

inputs = {
  project_id                = local.project_id
  activate_apis             = local.activate_apis
}
