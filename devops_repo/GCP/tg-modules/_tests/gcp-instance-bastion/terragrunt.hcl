include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-instance-bastion.hcl"
  expose = true
}

locals {
  google_tf_source_ref              = "v10.1.0"
  gcp_tf_source_firewall_policy     = "compute_instance"
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/${local.gcp_tf_source_firewall_policy}?ref=${local.google_tf_source_ref}"
}









