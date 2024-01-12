data "google_secret_manager_secret_version" "secret-version" {
  for_each  = local.my_secrets
  project   = var.project_id
  secret    = "${each.key}"
}

locals {
  my_secrets =  toset(var.secrets)
}