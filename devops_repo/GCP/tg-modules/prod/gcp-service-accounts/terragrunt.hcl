terraform {
  source = "${include.env.locals.source_base_url}?ref=v0.2.0"
}

include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gcp-service-accounts.hcl"
  expose = true
}