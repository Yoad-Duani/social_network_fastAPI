package main

###   General ENV   ###
deny[msg] {
    not input.locals.global_env
    msg = "Missing 'global_env' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.env
    msg = "Missing 'env' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_project_id
    msg = "Missing 'gcp_project_id' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_project_name
    msg = "Missing 'gcp_project_name' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_sa_prefix
    msg = "Missing 'gcp_sa_prefix' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_network_project_id
    msg = "Missing 'gcp_network_project_id' variable in Terragrunt env.hcl"
}


###   Compute Engine ENV   ###
deny[msg] {
    not input.locals.gcp_image_project_id
    msg = "Missing 'gcp_image_project_id' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_bastion_source_image
    msg = "Missing 'gcp_bastion_source_image' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_bastion_macine_type
    msg = "Missing 'gcp_bastion_macine_type' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_enable_shielded_vm
    msg = "Missing 'gcp_enable_shielded_vm' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_shielded_instance_config
    msg = "Missing 'gcp_shielded_instance_config' variable in Terragrunt env.hcl"
}


### GKE ENV ###
deny[msg] {
    not input.locals.gke_version_channel
    msg = "Missing 'gke_version_channel' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_version_prefix
    msg = "Missing 'gke_version_prefix' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_http_load_balancing
    msg = "Missing 'gke_http_load_balancing' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_network_policy
    msg = "Missing 'gke_network_policy' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_horizontal_pod_autoscaling
    msg = "Missing 'gke_horizontal_pod_autoscaling' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_filestore_csi_driver
    msg = "Missing 'gke_filestore_csi_driver' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_enable_private_endpoint
    msg = "Missing 'gke_enable_private_endpoint' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_enable_private_nodes
    msg = "Missing 'gke_enable_private_nodes' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_regional
    msg = "Missing 'gke_regional' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_logging_enabled_components
    msg = "Missing 'gke_logging_enabled_components' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_ip_masq_link_local
    msg = "Missing 'gke_ip_masq_link_local' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_configure_ip_masq
    msg = "Missing 'gke_configure_ip_masq' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_default_max_pods_per_node
    msg = "Missing 'gke_default_max_pods_per_node' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_create_service_account
    msg = "Missing 'gke_create_service_account' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_remove_default_node_pool
    msg = "Missing 'gke_remove_default_node_pool' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_enable_shielded_nodes
    msg = "Missing 'gke_enable_shielded_nodes' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_initial_node_count
    msg = "Missing 'gke_initial_node_count' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_machine_type
    msg = "Missing 'gke_machine_type' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_gce_pd_csi_driver
    msg = "Missing 'gke_gce_pd_csi_driver' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_deploy_using_private_endpoint
    msg = "Missing 'gke_deploy_using_private_endpoint' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_release_channel
    msg = "Missing 'gke_release_channel' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_deletion_protection
    msg = "Missing 'gke_deletion_protection' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_ip_range_pods_name
    msg = "Missing 'gke_ip_range_pods_name' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_ip_range_services_name
    msg = "Missing 'gke_ip_range_services_name' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gke_master_authorized_networks
    msg = "Missing 'gke_master_authorized_networks' variable in Terragrunt env.hcl"
}


###   Services Accounts ENV   ###
deny[msg] {
    not input.locals.gcp_sa_roles
    msg = "Missing 'gcp_sa_roles' variable in Terragrunt env.hcl"
}


###   GCP API Services ENV   ###
deny[msg] {
    not input.locals.gcp_api_services
    msg = "Missing 'gcp_api_services' variable in Terragrunt env.hcl"
}


###   Firewall Ruels ENV   ###
deny[msg] {
    not input.locals.gcp_firewall_policy_description
    msg = "Missing 'gcp_api_services' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.locals.gcp_firewall_policy_rules
    msg = "Missing 'gcp_firewall_policy_rules' variable in Terragrunt env.hcl"
}


###   VPC Routes   ###
deny[msg] {
    not input.locals.gcp_vpc_routes
    msg = "Missing 'gcp_vpc_routes' variable in Terragrunt env.hcl"
}
