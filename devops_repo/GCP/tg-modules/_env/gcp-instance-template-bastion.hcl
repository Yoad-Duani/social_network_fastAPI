
dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-service-accounts"]
}


locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                      = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                    = local.env_vars.locals.global_env.locals

  account_vars                  = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  google_tf_source_url              = local.env_global.google_tf_source_url
  google_tf_source_provider         = local.env_global.google_tf_source_provider
  google_tf_source_module           = "terraform-google-vm"

  org                           = local.account_vars.locals.org
  env_name                      = local.env_vars.locals.env
  gcp_project_id                = local.env_vars.locals.gcp_project_id
  gcp_project_name              = local.env_vars.locals.gcp_project_name
  gcp_default_zone              = local.env_global.gcp_default_zone
  gcp_region                    = local.env_global.gcp_region
  gcp_sa_prefix                       = local.env_vars.locals.gcp_sa_prefix
  gcp_node_subnet_name          = "${local.env_global.gcp_node_subnet_name}-${local.env_name}-general"
  gcp_network_project_id        = local.env_vars.locals.gcp_network_project_id
  gcp_image_project_id          = local.env_vars.locals.gcp_image_project_id
  gcp_bastion_source_image      = local.env_vars.locals.gcp_bastion_source_image
  gcp_bastion_macine_type       = local.env_vars.locals.gcp_bastion_macine_type
  gcp_service_account           = "${local.gcp_sa_prefix}-project-sa@${local.gcp_project_id}.iam.gserviceaccount.com"
  gcp_enable_shielded_vm        = local.env_vars.locals.gcp_enable_shielded_vm
  gcp_shielded_instance_config  = local.env_vars.locals.gcp_shielded_instance_config
  gcp_boot_disk_size_gb         = local.env_global.gcp_boot_disk_size_gb

  service_account   = {
    email = local.gcp_service_account
    scopes = ["cloud-platform"]
  }
}


inputs = {
  name_prefix                 = "${local.gcp_project_name}-${local.env_name}-bastion"
  region                      = local.gcp_region
  project_id                  = local.gcp_project_id
  subnetwork                  = local.gcp_node_subnet_name
  subnetwork_project          = local.gcp_network_project_id
  service_account             = local.service_account
  startup_script              = "${file("${get_terragrunt_dir()}/bootstrap.sh")}"
  enable_confidential_vm      = false
  tags                        = [
    "${local.gcp_project_id}",
    "${local.env_name}",
  ]

  //Boot Disk                 
  disk_size_gb                = "${local.gcp_boot_disk_size_gb}"
  disk_type                   = "pd-standard"
  auto_delete                 = false
  source_image                = local.gcp_bastion_source_image
  source_image_family         = "ubuntu-2204-lts"
  source_image_project        = local.gcp_image_project_id
  machine_type                = local.gcp_bastion_macine_type
  enable_shielded_vm          = local.gcp_enable_shielded_vm
  shielded_instance_config    = local.gcp_shielded_instance_config

}
