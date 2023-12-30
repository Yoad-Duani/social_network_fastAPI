include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../_env/helm-chart-argocd.hcl"
  expose = true
}

locals {
 base_source_ref                 = "main"
 base_tf_source_helm_chart       = "helm-chart"
}

terraform {
  source = "${include.env.locals.base_source_url}/${include.env.locals.base_source_module}//${include.env.locals.base_source_provider}/${local.base_tf_source_helm_chart}?ref=${local.base_source_ref}"
}