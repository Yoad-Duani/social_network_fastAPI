# ------------------------------------------------------------------------------
# Global Terragrunt Configuration
# ------------------------------------------------------------------------------

locals {

    # Load global env and environment variables according to the environment (prod, dev...)
    env_vars          = read_terragrunt_config(find_in_parent_folders("env.hcl"))
    env_global        = local.env_vars.locals.global_env.locals
    account_vars      = read_terragrunt_config(find_in_parent_folders("account.hcl"))
    #env_vars         = read_terragrunt_config(find_in_parent_folders("env.hcl"))

    org               = local.account_vars.locals.org
    gcp_region        = local.env_global.gcp_region
    project_id        = local.env_vars.locals.gcp_project_id
}

remote_state {
  backend = "gcs"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket              = "${get_env("TG_BUCKET_PREFIX", "tf-bucket")}-terraform-state-${local.gcp_region}-${local.project_id}"
    prefix              = "${path_relative_to_include()}/terraform.tfstate"
    location            = "${local.gcp_region}"
    project             = "${local.project_id}"
    gcs_bucket_labels   = {
        org =   "${local.org}"
    }
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "google" {
  #credentials = file("~/.config/gcloud/application_default_credentials.json")
  #credentials = file("/mnt/c/projects/data/GCP/gcp.yoad/test-deploy-392912-39c2fdcced89.json")
  project     = "${local.project_id}"
  region      = "${local.gcp_region}"
}
EOF
}