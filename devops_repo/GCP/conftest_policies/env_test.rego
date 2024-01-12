package main

deny[msg] {
    not input.include.env.locals.global_env
    msg = "Missing 'global_env' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.env
    msg = "Missing 'env' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_project_id
    msg = "Missing 'gcp_project_id' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_project_name
    msg = "Missing 'gcp_project_name' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_sa_prefix
    msg = "Missing 'gcp_sa_prefix' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_network_project_id
    msg = "Missing 'gcp_network_project_id' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_image_project_id
    msg = "Missing 'gcp_image_project_id' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_bastion_source_image
    msg = "Missing 'gcp_bastion_source_image' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_bastion_macine_type
    msg = "Missing 'gcp_bastion_macine_type' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_enable_shielded_vm
    msg = "Missing 'gcp_enable_shielded_vm' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gcp_shielded_instance_config
    msg = "Missing 'gcp_shielded_instance_config' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_version_channel
    msg = "Missing 'gke_version_channel' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_version_prefix
    msg = "Missing 'gke_version_prefix' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_http_load_balancing
    msg = "Missing 'gke_http_load_balancing' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_network_policy
    msg = "Missing 'gke_network_policy' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_horizontal_pod_autoscaling
    msg = "Missing 'gke_horizontal_pod_autoscaling' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_filestore_csi_driver
    msg = "Missing 'gke_filestore_csi_driver' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_enable_private_endpoint
    msg = "Missing 'gke_enable_private_endpoint' variable in Terragrunt env.hcl"
}

deny[msg] {
    not input.include.env.locals.gke_enable_private_nodes
    msg = "Missing 'gke_enable_private_nodes' variable in Terragrunt env.hcl"
}