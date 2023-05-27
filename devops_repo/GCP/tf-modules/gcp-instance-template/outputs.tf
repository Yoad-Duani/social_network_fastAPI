
output "self_link" {
  description = "self link of instance template"
  value       = google_compute_instance_template.tpl.self_link 
}

output "name" {
  description = "name of the instance template"
  value       = google_compute_instance_template.tpl.self_link 
}

output "tags" {
  description = "tags that will be associated with instance"
  value       = google_compute_instance_template.tpl.tags 
}