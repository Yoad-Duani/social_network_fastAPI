
dependencies {
  paths = ["${get_terragrunt_dir()}/../gcp-vpc", "${get_terragrunt_dir()}/../gcp-subnets", "${get_terragrunt_dir()}/../gcp-project-services", "${get_terragrunt_dir()}/../gcp-gke-version",  "${get_terragrunt_dir()}/../gcp-service-accounts"]
}

dependency "gcp-gke-version" {
  config_path = "${get_terragrunt_dir()}/../gcp-gke-version"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "init"]
  mock_outputs = {
    available_zones_names = [
        "me-west1-a",
        "me-west1-b"
    ]
    version = "1.27.3-gke.100"
  }
  mock_outputs_merge_strategy_with_state = "shallow"
  skip_outputs = false
}

dependency "gcp-vpc" {
  config_path = "${get_terragrunt_dir()}/../gcp-vpc"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "init"]
  mock_outputs = {
    network_name = "fake-name"
    network_id   = "fake-netwotk-id" 
  }
  mock_outputs_merge_strategy_with_state = "shallow"
}


dependency "gcp-subnets" {
  config_path = "${get_terragrunt_dir()}/../gcp-subnets"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "init"]
  mock_outputs = {
    subnets = {
      "fake-subnet" = {
        name = "fake-subnet"
        subnet_ip = "fake-ip1"
        subnet_region = "fake-region1"
        subnet_private_access = "false"
        subnet_private_ipv6_access = null
        subnet_flow_logs = "false"
        subnet_flow_logs_interval = "INTERVAL_5_SEC"
        subnet_flow_logs_sampling = "0.5"
        subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
        subnet_flow_logs_filter = "true"
        subnet_flow_logs_metadata_fields = []
        description = null
        purpose = null
        role = null
        stack_type = null
        ipv6_access_type = null
      }
    }
  }
  mock_outputs_merge_strategy_with_state = "shallow"
  skip_outputs = true
  
}

dependency "gcp-service-accounts" {
  config_path = "${get_terragrunt_dir()}/../gcp-service-accounts"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "init"]
  mock_outputs_merge_strategy_with_state = "shallow"
  mock_outputs = {
    network_name = "fake-name" 
  }
  skip_outputs = true
}

locals {
  # Load global env and environment variables according to the environment (prod, dev...)
  env_vars                            = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env_global                          = local.env_vars.locals.global_env.locals

  #gke_node_service_account            = dependency.gcp-service-accounts.outputs.email[1]

  google_tf_source_url              = local.env_global.google_tf_source_url
  google_tf_source_provider         = local.env_global.google_tf_source_provider
  google_tf_source_module           = "terraform-google-kubernetes-engine"

  env_name                            = local.env_vars.locals.env
  gcp_project_id                      = local.env_vars.locals.gcp_project_id
  gcp_project_name                    = local.env_vars.locals.gcp_project_name
  gcp_region                          = local.env_global.gcp_region
  gcp_default_zone                    = local.env_global.gcp_default_zone
  gcp_region_zones                    = local.env_global.gcp_region_zones
  gcp_sa_prefix                       = local.env_vars.locals.gcp_sa_prefix
  #gcp_vpc_name                        = dependency.gcp-vpc.outputs.network_name
  #gke_node_subnet_name                = dependency.gcp-subnets.outputs.subnets[1].subnet_name
  gke_master_ipv4_cidr_block          = local.env_global.gke_master_ipv4_cidr_block
  gke_http_load_balancing             = local.env_vars.locals.gke_http_load_balancing
  gke_network_policy                  = local.env_vars.locals.gke_network_policy  
  gke_horizontal_pod_autoscaling      = local.env_vars.locals.gke_horizontal_pod_autoscaling 
  gke_filestore_csi_driver            = local.env_vars.locals.gke_filestore_csi_driver 
  gke_enable_private_endpoint         = local.env_vars.locals.gke_enable_private_endpoint
  gke_enable_private_nodes            = local.env_vars.locals.gke_enable_private_nodes
  gke_regional                        = local.env_vars.locals.gke_regional
  gke_master_authorized_networks      = local.env_vars.locals.gke_master_authorized_networks
  gke_logging_service                 = local.env_global.gke_logging_service
  gke_logging_enabled_components      = local.env_vars.locals.gke_logging_enabled_components
  gke_ip_masq_link_local              = local.env_vars.locals.gke_ip_masq_link_local
  gke_configure_ip_masq               = local.env_vars.locals.gke_configure_ip_masq
  gke_default_max_pods_per_node       = local.env_vars.locals.gke_default_max_pods_per_node
  gke_create_service_account          = local.env_vars.locals.gke_create_service_account
  gke_remove_default_node_pool        = local.env_vars.locals.gke_remove_default_node_pool
  gke_enable_shielded_nodes           = local.env_vars.locals.gke_enable_shielded_nodes
  gke_initial_node_count              = local.env_vars.locals.gke_initial_node_count
  gke_machine_type                    = local.env_vars.locals.gke_machine_type
  gke_gce_pd_csi_driver               = local.env_vars.locals.gke_gce_pd_csi_driver
  gke_deploy_using_private_endpoint   = local.env_vars.locals.gke_deploy_using_private_endpoint
  gke_ip_range_pods                   = local.env_global.gke_ip_range_pods
  gke_ip_range_services               = local.env_global.gke_ip_range_services
  gke_ip_range_pods_name              = local.env_vars.locals.gke_ip_range_pods_name
  gke_ip_range_services_name          = local.env_vars.locals.gke_ip_range_services_name
  gke_release_channel                 = local.env_vars.locals.gke_release_channel
  gke_deletion_protection             = local.env_vars.locals.gke_deletion_protection
  gke_service_account                 = "${local.gcp_sa_prefix}-project-sa@${local.gcp_project_id}.iam.gserviceaccount.com"
  

}

inputs = {  
  name                          = "${local.gcp_project_id}-${local.env_name}-gke"
  project_id                    = local.gcp_project_id
  region                        = local.gcp_region
  regional                      = local.gke_regional
  kubernetes_version            = dependency.gcp-gke-version.outputs.version
  zones                         = local.gcp_region_zones
  network                       = dependency.gcp-vpc.outputs.network_name
  #network                       = "${local.env_global.gcp_vpc_name}-${local.env_vars.locals.gcp_project_id}-${local.env_name}"
  #network                       = "projects/${local.gcp_project_id}/global/networks/${local.env_global.gcp_vpc_name}-${local.env_vars.locals.gcp_project_id}-${local.env_name}"
  // subnetwork                    = dependency.gcp-subnets.outputs.subnets["${local.gcp_region}/${local.env_global.gke_node_subnet_name}-${local.env_name}-gke"].name
  // subnetwork                    = dependency.gcp-subnets.outputs.subnets[0].name
  subnetwork                    = "${local.env_global.gke_node_subnet_name}-${local.env_name}-gke"
  #network_project_id            = dependency.gcp-vpc.outputs.network_id
  network_project_id            = local.gcp_project_id
  ip_range_pods                 = local.gke_ip_range_pods_name
  ip_range_services             = local.gke_ip_range_services_name
  master_authorized_networks    = local.gke_master_authorized_networks
  master_ipv4_cidr_block        = local.gke_master_ipv4_cidr_block
  http_load_balancing           = local.gke_http_load_balancing
  network_policy                = local.gke_network_policy
  horizontal_pod_autoscaling    = local.gke_horizontal_pod_autoscaling
  filestore_csi_driver          = local.gke_filestore_csi_driver
  enable_private_endpoint       = local.gke_enable_private_endpoint
  enable_private_nodes          = local.gke_enable_private_nodes
  ip_masq_link_local            = local.gke_ip_masq_link_local
  configure_ip_masq             = local.gke_configure_ip_masq
  default_max_pods_per_node     = local.gke_default_max_pods_per_node
  create_service_account        = local.gke_create_service_account
  remove_default_node_pool      = local.gke_remove_default_node_pool
  enable_shielded_nodes         = local.gke_enable_shielded_nodes
  initial_node_count            = local.gke_initial_node_count
  machine_type                  = local.gke_machine_type
  gce_pd_csi_driver             = local.gke_gce_pd_csi_driver
  deploy_using_private_endpoint = local.gke_deploy_using_private_endpoint
  # logging_service             = local.gke_logging_service
  # logging_enabled_components  = local.gke_logging_enabled_components
  service_account               = local.gke_service_account
  release_channel               = local.gke_release_channel
  deletion_protection           = local.gke_deletion_protection

  node_pools                    = [
    {
      name                      = "${local.gcp_project_name}-management"
      machine_type              = "e2-standard-2"
      min_count                 = 1
      max_count                 = 1
      local_ssd_count           = 0
      disk_size_gb              = 80
      disk_type                 = "pd-standard"
      image_type                = "COS_CONTAINERD"
      auto_repair               = true
      auto_upgrade              = false
      #service_account           = dependency.gcp-service-accounts.outputs.email["${local.gcp_sa_prefix}-project-sa"]
      service_account           = local.gke_service_account
      preemptible               = false
      initial_node_count        = 1
      enable_secure_boot        = true
    },
    {
      name                      = "${local.gcp_project_name}-services"
      machine_type              = "e2-standard-2"
      min_count                 = 1
      max_count                 = 2
      local_ssd_count           = 0
      disk_size_gb              = 80
      disk_type                 = "pd-standard"
      image_type                = "COS_CONTAINERD"
      auto_repair               = true
      auto_upgrade              = false
      service_account           = local.gke_service_account
      preemptible               = false
      initial_node_count        = 1
      enable_secure_boot        = true
    },
    {
      name                      = "${local.gcp_project_name}-stateful"
      machine_type              = "e2-standard-2"
      min_count                 = 1
      max_count                 = 1
      local_ssd_count           = 0
      disk_size_gb              = 80
      disk_type                 = "pd-standard"
      image_type                = "COS_CONTAINERD"
      auto_repair               = true
      auto_upgrade              = false
      service_account           = local.gke_service_account
      preemptible               = false
      initial_node_count        = 1
      enable_secure_boot        = true
    },
  ]

  node_pools_tags = {
    all = [
      "${local.env_name}",
      "${local.gcp_project_id}"
    ]
  }

  node_pools_labels = {
    all = {
      env = "${local.env_name}"
    }

    "${local.gcp_project_name}-management" = {
      "${local.gcp_project_name}" = "management"
    }

    "${local.gcp_project_name}-services" = {
      "${local.gcp_project_name}" = "services"
    }

    "${local.gcp_project_name}-stateful" = {
      "${local.gcp_project_name}" = "stateful"
    }

    default-node-pool = {
      default-node-pool = true
      node-pool = "${local.gcp_project_name}-management"
    }
  }

  node_pools_taints = {
    # "${local.gcp_project_name}-management" = [
    #   {
    #     key    = "gke-node-pool"
    #     value  = "${local.gcp_project_name}-management"
    #     effect = "NO_SCHEDULE"
    #   },
    # ]

    "${local.gcp_project_name}-services" = [
      {
        key    = "gke-node-pool"
        value  = "${local.gcp_project_name}-services"
        effect = "NO_SCHEDULE"
      },
    ]

    "${local.gcp_project_name}-stateful" = [
      {
        key    = "gke-node-pool"
        value  = "${local.gcp_project_name}-stateful"
        effect = "NO_SCHEDULE"
      },
    ]
  }

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}