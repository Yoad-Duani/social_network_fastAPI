dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts", "${get_terragrunt_dir()}/../gcp-gke"]
}

dependency "gcp-gke" {
  config_path = "${get_terragrunt_dir()}/../gcp-gke"
  mock_outputs_allowed_terraform_commands = ["validate", "init", "plan"]
  mock_outputs = {
    name            = "fake-name"
    endpoint        = "10.10.10.10"
    ca_certificate  = ""
  }
  skip_outputs = false
  mock_outputs_merge_strategy_with_state = "shallow"
}

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                        = local.env_vars.locals.global_env.locals

  base_source_url                   = local.env_global.base_source_url
  base_source_module                = local.env_global.base_source_module
  base_source_provider              = local.env_global.base_source_provider

  env_name                          = local.env_vars.locals.env
  gcp_project_id                    = local.env_vars.locals.gcp_project_id
  gcp_project_name                  = local.env_vars.locals.gcp_project_name

  argocd_chart_name                 = local.env_vars.locals.argocd_chart_name
  argocd_chart_version              = local.env_vars.locals.argocd_chart_version
  argocd_chart_repository           = local.env_vars.locals.argocd_chart_repository
  argocd_values_file_path           = local.env_vars.locals.argocd_values_file_path

}

inputs = {
  gke_name                    = dependency.gcp-gke.outputs.name
  gke_endpoint                = dependency.gcp-gke.outputs.endpoint
  gke_ca_cert                 = dependency.gcp-gke.outputs.ca_certificate

  enabled                     = true
  name                        = "argo"
  namespace                   = "argocd"
  chart                       = local.argocd_chart_name
  chart_version               = local.argocd_chart_version
  repository                  = local.argocd_chart_repository
  values_file_path            = local.argocd_values_file_path
}