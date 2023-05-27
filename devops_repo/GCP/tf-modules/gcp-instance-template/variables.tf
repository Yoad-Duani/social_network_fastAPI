

variable "project_id" {
  type        = string
  description = "The GCP project ID"
  default     = null
}

variable "name_prefix" {
  description = "Name prefix for instance template"
  default     = "default=instance-template"
}

variable "machine_type" {
  description = "Machine type to create, e.g n1-standard-1"
  default     = "n1-standard-1"
  # n1-standard-1 - monthly estimate $27.82 
}

variable "min_cpu_platform" {
  description = "Specifies a minium cpu platform"
  type        = string
  default     = null
}

variable "can_ip_forward" {
  description = "Enable IP forwarding"
  default     = "fasle"
}

variable "tags" {
  type        = list(string)
  description = "Network tags, provided as list"
  default     = []
}

variable "labels" {
  type        = map(string)
  description = "Labels, provided as map"
  default     = {}
}

variable "preemptible" {
  type        = bool
  description = "Allow the instance to be preempted"
  default     = false
}

variable "on_host_maintenance" {
  type        = string
  description = "Inctance availability policy"
  default     = null
}

variable "region" {
  type        = string
  description = "region where the instance template should be created"
  default     = null
}




#################
##    Disk     ##
#################

variable "source_image" {
  description = "Source disk image. defalt is latest public CentOS image"
  default     = ""
}

variable "source_image_family" {
  description = "Source image family."
  default     = "centos-stream-9"
}

variable "source_image_project" {
  description = "Source image project."
  default     = "centos-cloud"
}

variable "disk_size_gb" {
  description = "Boot disk size in GB."
  default     = "30"
}

variable "disk_type" {
  description = "Boot disk type, can be either pd-ssd, local-ssd, or pd-standard"
  default     = "pd-standard"
}

variable "disk_labels" {
  description = "Labels to be assigned to boot disk, provided as a map."
  type        = map(string)
  default     = {}
}

variable "disk_encryption_key" {
  description = "The id of the encryption key that is stored in Google Cloud KMS to use to encrypt all the disks on this instance"
  type        = map(string)
  default     = {}
}

variable "auto_delete" {
  description = "Whether or not the boot disk should be auto-deleted"
  default     = "true"
}

variable "additional_disks" {
  description = "List of maps of additional disks. See https://www.terraform.io/docs/providers/google/r/compute_instance_template#disk_name"
  type = list(object({
    disk_name    = string
    device_name  = string
    auto_delete  = bool
    boot         = bool
    disk_size_gb = number
    disk_type    = string
    disk_labels  = map(string)
  }))
  default     = {}
}



##########################
##  Network Interface   ##
##########################

variable "network" {
  description = "The name or self_link of the network to attach this interface to. Use network attribute for Legacy or Auto subnetted networks and subnetwork for custom subnetted networks."
  default     = ""
}

variable "subnetwork" {
  description = "The name of the subnetwork to attach this interface to. The subnetwork must exist in the same region this instance will be created in. Either network or subnetwork must be provided."
  default     = ""
}

variable "subnetwork_project" {
  description = "The ID of the project in which the subnetwork belongs. If it is not provided, the provider project is used."
  default     = ""
}

variable "network_ip" {
  description = "Private IP address to assign to the instance if desired."
  default     = ""
}



########################
##  Service Account  ##
########################

variable "service_account" {
  description = "Service account to attach to the instance. See https://www.terraform.io/docs/providers/google/r/compute_instance_template#service_account."
  type = object({
    email  = string
    scopes = set(string)
  })
}



#####################
##    Metadata     ##
#####################

variable "startup_script" {
  description = "Startup script to run when instance spin up"
  default     = {}
}

variable "metadata" {
  type        = map(string)
  description = "Metadata, provided as a map"
  default     = {}
}



#####################
##  Shielded VMs   ##
#####################

variable "enable_shielded_vm" {
  type        = bool
  description = "Whether to enable the Shielded VM configuration on the instance. Note that the instance image must support Shielded VMs. See https://cloud.google.com/compute/docs/images"
  default     = false
}

variable "shielded_instance_config" {
  description = "Not used unless enable_shielded_vm is true. Shielded VM configuration for the instance."
  type = object({
    enable_secure_boot          = bool
    enable_vtpm                 = bool
    enable_integrity_monitoring = bool
  })
  default     = {
  "enable_integrity_monitoring": true,
  "enable_secure_boot": true,
  "enable_vtpm": true
  }
}



#################################
##  Confidential Compute Vms   ##
#################################

variable "enable_confidential_vm" {
  type        = bool
  description = "Whether to enable the Confidential VM configuration on the instance. Note that the instance image must support Confidential VMs. See https://cloud.google.com/compute/docs/images"
  default     = false
}



####################
##   Public IP    ##
####################

variable "access_config" {
  description = "Access configurations, i.e. IPs via which the VM instance can be accessed via the Internet."
  type = list(object({
    nat_ip       = string
    network_tier = string
  }))
  default     = []
}



################################
##  Guest Accelerator (GPU)   ##
################################

variable "gpu" {
  description = "GPU information. Type and count of GPU to attach to the instance template. See https://cloud.google.com/compute/docs/gpus more details"
  type        = object({
    type  = string
    count = number
  })
  default     = null
}