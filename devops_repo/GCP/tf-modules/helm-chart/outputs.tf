
output "release_name" {
  value = helm_release.this-helm[0].name
}

output "version" {
  value = helm_release.this-helm[0].version
}

output "values" {
  value = helm_release.this-helm[0].values
}