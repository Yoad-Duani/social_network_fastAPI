
locals {
  my_secrets_id =  toset(var.secrets_id)
}

resource "random_string" "prefix_username" {
  count   = length(local.my_secrets_id)
  length  = 3
  special = false
}

resource "random_string" "secret_password" {
  count   = length(local.my_secrets_id)
  length  = 12
  special = true
}

resource "google_secret_manager_secret" "my-secret" {
    for_each  = local.my_secrets_id
    secret_id = each.key
    project = var.project_id
    labels = {
      env = var.env_name
    }
    replication {
        auto{}    
    }
}

resource "google_secret_manager_secret_version" "secret-version" {
    for_each = local.my_secrets_id
    secret = each.value

    secret_data = jsonencode({
        username = format("user0%s", element(random_string.prefix_username.*.result, index(local.my_secrets_id, each.value))),
        password = element(random_string.secret_password.*.result, index(local.my_secrets_id, each.value)),
    }) 
}
