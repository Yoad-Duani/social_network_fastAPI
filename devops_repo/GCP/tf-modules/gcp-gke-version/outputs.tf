output "version" {
  value       = data.google_container_engine_versions.channel.release_channel_latest_version[var.gke_version_channel]
}

output "available_zones_names" {
  value       = data.google_compute_zones.available.names

}