dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts", "${get_terragrunt_dir()}/../gcp-secrets-data-postgresql"]
}

dependency "gcp-secret-data" {
  config_path = "${get_terragrunt_dir()}/../gcp-secrets-data-postgresql"
  mock_outputs_allowed_terraform_commands = ["validate", "init"]
  mock_outputs = {
    secrets = ["fake_secrets"]
  }
  mock_outputs_merge_strategy_with_state = "shallow"
}

dependency "gcp-vpc" {
  config_path = "${get_terragrunt_dir()}/../gcp-vpc"
  mock_outputs_allowed_terraform_commands = ["validate", "init"]
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

  postgresql_secrets                  = local.env_global.read_secrets_postgresql[0]

}


inputs = {
  name                      = "$postgresql-{local.gcp_project_name}-${local.env_name}"
  project_id                = local.gcp_project_id
  region                    = local.gcp_region

  user_name                 = lookup(lookup(dependency.gcp-secret-data.outputs.secrets,local.postgresql_secrets,jsondecode("{\"username\": \"somthing_went_worng\"}")),"username","somthing_went_worng")
  user_password             = lookup(lookup(dependency.gcp-secret-data.outputs.secrets,local.postgresql_secrets,jsondecode("{\"password\": \"somthing_went_worng\"}")),"password","somthing_went_worng")

  root_password             = "test123"
  disk_size                 = 40
  database_version          = "POSTGRES_15"
  #database_flags            =

  ip_configuration          = {
    "require_ssl"           = false
    "ipv4_enabled"          = false
    "allocated_ip_range"    = "172.23.16.0/20"
    "private_network"       = "projects/${local.project_id}/global/networks/${dependency.gcp-vpc.outputs.network_name}"
  }
  tier                      = "db-n1-standard-1"
  db_name                   = "fastapi"
}