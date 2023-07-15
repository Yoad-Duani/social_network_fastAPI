terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//?ref=${local.google_tf_source_ref}"
}

locals {
  google_tf_source_ref              = "v4.2.1"
}

include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-service-accounts.hcl"
  expose = true
}