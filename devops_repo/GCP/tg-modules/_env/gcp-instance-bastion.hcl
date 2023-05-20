//terraform {
//  source = "github.com/<org>/modules.git//app?ref=v0.1.0" ### source for instance
//}

terraform {
  source = "${local.google_tf_source_url}"
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_name = local.env_vars.locals.env
  base_source_module = "gcp-instance"
  source_base_url = "github.com/<org>/modules.git//app"
}

inputs = {
  env            = local.env_name
  basename       = "example-app-${local.env_name}"
}