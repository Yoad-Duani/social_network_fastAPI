dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts", "${get_terragrunt_dir()}/../gcp-firewall-policy", "${get_terragrunt_dir()}/../gcp-cloud-router-nat", "${get_terragrunt_dir()}/../gcp-instance-template-bastion"]
}

# dependency "gcp-vpc" {
#   config_path = "${get_terragrunt_dir()}/../gcp-vpc"
#   mock_outputs_allowed_terraform_commands = ["validate"]
#   mock_outputs = {
#     network_name = "fake-name"
#   }
#   mock_outputs_merge_strategy_with_state = "shallow"
# }

dependency "gcp-instance-template-bastion" {
  config_path = "${get_terragrunt_dir()}/../gcp-instance-template-bastion"
  mock_outputs_allowed_terraform_commands = ["validate", "init", "plan"]
  mock_outputs = {
    self_link = "project/foo/bar"
  }
  mock_outputs_merge_strategy_with_state = "shallow"
}

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                        = local.env_vars.locals.global_env.locals

  google_tf_source_url              = local.env_global.google_tf_source_url
  google_tf_source_provider         = local.env_global.google_tf_source_provider
  google_tf_source_module           = "terraform-google-vm"

  env_name                          = local.env_vars.locals.env
  gcp_project_id                    = local.env_vars.locals.gcp_project_id
  gcp_project_name                  = local.env_vars.locals.gcp_project_name
  gcp_region                        = local.env_global.gcp_region
  gcp_zone                          = "${local.gcp_region}-${local.env_global.gcp_default_zone}"

}

inputs = {
  region                = local.gcp_region
  zone                  = local.gcp_zone
  num_instances         = 1
  instance_template     = dependency.gcp-instance-template-bastion.outputs.self_link
  add_hostname_suffix	  = false
}