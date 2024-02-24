
// dependency "gcp-vpc" {
//   config_path = "${get_terragrunt_dir()}/../gcp-project-services"
//   mock_outputs_allowed_terraform_commands = ["validate", "init", "plan"]
//   skip_outputs = true
//   mock_outputs_merge_strategy_with_state = "shallow"
// }

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars              = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global            = local.env_vars.locals.global_env.locals

  google_tf_source_url              = local.env_global.google_tf_source_url
  google_tf_source_provider         = local.env_global.google_tf_source_provider
  google_tf_source_module           = "terraform-google-service-accounts"

  env_name              = local.env_vars.locals.env
  project_id            = local.env_vars.locals.gcp_project_id
  gcp_sa_prefix         = local.env_vars.locals.gcp_sa_prefix
  gcp_sa_roles          = local.env_vars.locals.gcp_sa_roles
  gcp_sa_names          = local.env_global.gcp_sa_names
  gcp_sa_description    = local.env_global.gcp_sa_description

}

inputs = {
  project_id            = local.project_id
  prefix                = local.gcp_sa_prefix
  names                 = local.gcp_sa_names
  project_roles         = local.gcp_sa_roles
  description           = local.gcp_sa_description
  generate_keys         = true
}