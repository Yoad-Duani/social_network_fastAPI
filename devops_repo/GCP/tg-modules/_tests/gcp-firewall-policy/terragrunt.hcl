include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-firewall-policy.hcl"
  expose = true
}

locals {
  google_tf_source_ref              = "v8.0.0"
  gcp_tf_source_firewall_policy     = "network-firewall-policy"
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/${local.gcp_tf_source_firewall_policy}?ref=${local.google_tf_source_ref}"
}
