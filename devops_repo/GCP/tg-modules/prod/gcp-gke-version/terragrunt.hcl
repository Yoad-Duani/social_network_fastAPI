
include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-gke-version.hcl"
  expose = true
}

locals {
 base_source_ref              = "main"
}

terraform {
  source = "${include.env.locals.base_source_url}/${include.env.locals.base_source_module}//${include.env.locals.base_source_provider}/gcp-gke-version?ref=${local.base_source_ref}"
}

