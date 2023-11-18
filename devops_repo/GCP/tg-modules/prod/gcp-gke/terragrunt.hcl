include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-gke.hcl"
  expose = true
}

locals {
  google_tf_source_ref            = "29.0.0"
  gke_tf_source_module            = "beta-private-cluster"
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/${local.gke_tf_source_module}?ref=${local.google_tf_source_ref}"
}