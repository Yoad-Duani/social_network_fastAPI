
locals {
  my_secrets_id =  var.secrets_id
}

resource "random_string" "prefix_username" {
  count   = length(local.my_secrets_id)
  length  = 3
  special = false
  min_numeric = 3
}

resource "random_string" "secret_password" {
  count   = length(local.my_secrets_id)
  length  = 12
  special = true
  override_special = "@!"
}

resource "google_secret_manager_secret" "my-secret" {
    for_each  = toset(var.secrets_id)
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
    for_each = {for idx, secrets in local.my_secrets_id: secrets => idx}

    secret = google_secret_manager_secret.my-secret[each.key].id

    secret_data = jsonencode({
        username = format("user0%s", element(random_string.prefix_username.*.result, each.value)),
        password = element(random_string.secret_password.*.result,  each.value),
    }) 
}
