
dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc"]
}

dependency "gcp-vpc" {
  config_path = "${get_terragrunt_dir()}/../gcp-vpc"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "init"]
  mock_outputs = {
    network_name = "fake-name"
  }
  mock_outputs_merge_strategy_with_state = "shallow"
}

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                      = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                    = local.env_vars.locals.global_env.locals

  account_vars                  = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  env_name                      = local.env_vars.locals.env
  gcp_region                    = local.env_global.gcp_region

  google_tf_source_url          = local.env_global.google_tf_source_url
  google_tf_source_provider     = local.env_global.google_tf_source_provider
  google_tf_source_module       = "terraform-google-network"

  gcp_node_subnet_name          = "${local.env_global.gcp_node_subnet_name}-${local.env_name}-general"
  gcp_node_subnet_cidr          = local.env_global.gcp_node_subnet_cidr
  gcp_node_subnet_description   = local.env_global.gcp_node_subnet_description

  gke_node_subnet_name          = "${local.env_global.gke_node_subnet_name}-${local.env_name}-gke"
  gke_node_subnet_cidr          = local.env_global.gke_node_subnet_cidr
  gke_node_subnet_description   = local.env_global.gke_node_subnet_description

  gke_ip_range_pods             = local.env_global.gke_ip_range_pods
  gke_ip_range_services         = local.env_global.gke_ip_range_services
  gke_ip_range_pods_name        = local.env_vars.locals.gke_ip_range_pods_name
  gke_ip_range_services_name    = local.env_vars.locals.gke_ip_range_services_name


}

inputs = {
  project_id                = local.env_vars.locals.gcp_project_id
  network_name              = dependency.gcp-vpc.outputs.network_name
  subnets = [
    {
      subnet_name           = local.gcp_node_subnet_name
      subnet_ip             = local.gcp_node_subnet_cidr
      subnet_region         = local.gcp_region
      subnet_private_access = "true"
      subnet_flow_logs      = "false"
      description           = local.gcp_node_subnet_description
    },
    {
      subnet_name           = local.gke_node_subnet_name
      subnet_ip             = local.gke_node_subnet_cidr
      subnet_region         = local.gcp_region
      subnet_private_access = "true"
      subnet_flow_logs      = "false"
      description           = local.gke_node_subnet_description
    }
  ]

  secondary_ranges = {
        "${local.gke_node_subnet_name}" = [
            {
                range_name    = "${local.gke_ip_range_pods_name}"
                ip_cidr_range = "${local.gke_ip_range_pods}"
            },
            {
                range_name    = "${local.gke_ip_range_services_name}"
                ip_cidr_range = "${local.gke_ip_range_services}"
            }
        ]
    }
}