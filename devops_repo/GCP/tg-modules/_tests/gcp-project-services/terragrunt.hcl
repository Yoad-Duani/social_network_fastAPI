include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-project-services.hcl"
  expose = true
}

locals {
  google_tf_source_ref              = "v14.2.0"
}


terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/project_services?ref=${local.google_tf_source_ref}"
}