include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-cloud-router-nat.hcl"
  expose = true
}

locals {
  google_tf_source_ref              = "v6.0.2"
  # gcp_tf_source_     = ""
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//?ref=${local.google_tf_source_ref}"
}
