#terraform {
#  source = "${locals.google_tf_source_url}/${locals.google_tf_source_module}/${locals.google_tf_source_provider}/vpc?ref=${locals.google_tf_source_ref}"
#}


locals {

  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                        = local.env_vars.locals.global_env.locals

  env_name                          = local.env_vars.locals.env
  google_tf_source_url              = local.env_global.google_tf_source_url
  google_tf_source_provider         = local.env_global.google_tf_source_provider
  google_tf_source_module           = "terraform-google-network"
# google_tf_source_ref              = "7.0.0"

}


inputs = {
  project_id        = local.env_vars.locals.gcp_project_id
  network_name      = "${local.env_vars.locals.global_env.locals.gcp_vpc_name}-${local.env_name}"
  shared_vpc_host   = false
}