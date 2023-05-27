
#######################
##    Data Source    ##
#######################





##################
##    Locals    ##
##################

locals {
  boot_disk = [
    {
      source_image = var.source_image
    }
  ]
}


#########################
##  Instance Template  ##
#########################
resource "google_compute_instance_template" "instance_template" {
  name_prefix             = "${var.name_prefix}-"
  project                 = var.project_id
#   name                    = var.instance_name
#   instance_description    = "Instance template for my project"
  machine_type            = var.machine_type
  zone                    = var.instance_zone
  labels                  = var.labels
  metadata                = var.metadata
  tags                    = var.tags
  can_ip_forward          = var.can_ip_forward
  startup_script          = var.startup_script
  region                  = var.region
  min_cpu_platform        = var.min_cpu_platform


  network                 = google_compute_network.vpc_network.self_link
  subnetwork              = google_compute_subnetwork.subnet.self_link
  service_account {
    email = var.service_account_email
  }
  
  disk {
    source_image = "projects/debian-cloud/global/images/debian-10-buster-v20220923"
    auto_delete  = true
  }

  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {
      // Ephemeral IP configuration, can be customized as needed
    }
  }

  metadata {
    # Additional metadata for the instance
    startup-script = <<-EOF
      #!/bin/bash
      # Add any custom startup script here
    EOF
  }

#   tags = ["web-server", "backend"]
}