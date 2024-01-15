dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts", "${get_terragrunt_dir()}/../gcp-secrets-data-postgresql"]
}

dependency "gcp-secret-data" {
  config_path = "${get_terragrunt_dir()}/../gcp-secrets-data-postgresql"
  mock_outputs_allowed_terraform_commands = ["validate", "init", "plan"]
  mock_outputs = {
    secrets = {
    fake_secrets_key1 = "fake_secret_value1"
    fake_secrets_key2 = "fake_secret_value2"
  }
  }
  mock_outputs_merge_strategy_with_state = "shallow"
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

  postgresql_secrets                  = local.env_global.read_secrets_postgresql[0]

  gcp_cloud_sql_disk_size             = local.env_vars.locals.gcp_cloud_sql_disk_size
  gcp_cloud_sql_database_version      = local.env_vars.locals.gcp_cloud_sql_database_version
  gcp_cloud_sql_database_flags        = local.env_vars.locals.gcp_cloud_sql_database_flags
  gcp_cloud_sql_machine_type          = local.env_vars.locals.gcp_cloud_sql_machine_type
  gcp_cloud_sql_db_name               = local.env_vars.locals.gcp_cloud_sql_db_name

  gcp_cloud_sql_ip_configuration_require_ssl  = local.env_vars.locals.gcp_cloud_sql_ip_configuration_require_ssl
  gcp_cloud_sql_ip_configuration_ipv4_enabled = local.env_vars.locals.gcp_cloud_sql_ip_configuration_ipv4_enabled
}

inputs = {
  name                      = "$postgresql-{local.gcp_project_name}-${local.env_name}"
  project_id                = local.gcp_project_id
  region                    = local.gcp_region
  tier                      = local.gcp_cloud_sql_machine_type
  db_name                   = local.gcp_cloud_sql_db_name
  disk_size                 = local.gcp_cloud_sql_disk_size
  database_version          = local.gcp_cloud_sql_database_version

  user_name                 = lookup(lookup(dependency.gcp-secret-data.outputs.secrets,local.postgresql_secrets,jsondecode("{\"username\": \"somthing_went_worng\"}")),"username","somthing_went_worng")
  user_password             = lookup(lookup(dependency.gcp-secret-data.outputs.secrets,local.postgresql_secrets,jsondecode("{\"password\": \"somthing_went_worng\"}")),"password","somthing_went_worng")
  root_password             = "test123"
  
  #database_flags            =

  ip_configuration          = {
    "require_ssl"           = local.gcp_cloud_sql_ip_configuration_require_ssl
    "ipv4_enabled"          = local.gcp_cloud_sql_ip_configuration_ipv4_enabled
    "allocated_ip_range"    = "${local.env_global.gcp_allocated_ip_range_private_service_access}/${local.env_global.gcp_allocated_prefix_length_private_service_access}"
    "private_network"       = "projects/${local.gcp_project_id}/global/networks/${dependency.gcp-vpc.outputs.network_name}"
  }
}