include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-secrets-create.hcl"
  expose = true
}

locals {
 base_source_ref                 = "main"
 base_tf_source_secrets_create     = "gcp-secret-manager-create"
}

terraform {
  source = "${include.env.locals.base_source_url}/${include.env.locals.base_source_module}//${include.env.locals.base_source_provider}/${local.base_tf_source_secrets_create}?ref=${local.base_source_ref}"
}
