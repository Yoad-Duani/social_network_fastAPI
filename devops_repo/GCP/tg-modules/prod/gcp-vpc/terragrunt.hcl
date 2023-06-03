include {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/gpc-vpc.hcl"
#  path   = path_relative_to_include("../../_env/app.hcl")
#  path   = "${path_relative_to_include(../../)}/_env/gpc-vpc.hcl"
#  path   = path_relative_from_include() + "/../../_env/gpc-vpc.hcl"
#   path   = "${get_parent_terragrunt_dir(../)}"
  expose = true
}

# Construct the terraform.source
terraform {
  source = "${include.env.locals.google_tf_source_url}/${include.env.locals.google_tf_source_module}//${include.env.locals.google_tf_source_provider}/vpc?ref=v7.0.0"
}
