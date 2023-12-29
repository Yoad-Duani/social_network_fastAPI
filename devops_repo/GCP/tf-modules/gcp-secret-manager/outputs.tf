output "secrets" {
  value = { for k,v in data.google_secret_manager_secret_version.secret-version : k=>jsondecode(v)}
  sensitive = true
}