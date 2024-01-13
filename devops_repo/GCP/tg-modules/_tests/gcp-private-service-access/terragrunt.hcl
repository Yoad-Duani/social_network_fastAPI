include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-private-service-access.hcl"
  expose = true
}

locals {
  google_tf_source_ref                  = "v18.1.0"
  gcp_tf_source_private_service_access  = "private_service_access"
}

terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/${local.gcp_tf_source_private_service_access}?ref=${local.google_tf_source_ref}"
}