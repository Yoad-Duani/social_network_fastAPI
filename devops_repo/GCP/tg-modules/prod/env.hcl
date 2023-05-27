locals {
  global_env        = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env               = "prod"
  gcp_project_id    = "fastapi-387914"
  gcp_project_name  = "FastAPI"
}
