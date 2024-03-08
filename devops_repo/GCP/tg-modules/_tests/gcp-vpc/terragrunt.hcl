include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-vpc.hcl"
  expose = true
}

locals {
  google_tf_source_ref              = "v7.0.0"
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/vpc?ref=${local.google_tf_source_ref}"
}
