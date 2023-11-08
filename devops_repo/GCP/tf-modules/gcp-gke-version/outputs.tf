output "version" {
  value       = data.google_container_engine_versions.channel.release_channel_latest_version[var.gke_version_channel]
}

output "name" {
  description = "name of the instance template"
  value       = google_compute_instance_template.tpl.self_link 
}