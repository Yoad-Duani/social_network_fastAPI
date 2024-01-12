locals {
  /////   General ENV   /////
  global_env                    = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  env                           = "prod"
  gcp_project_id                = "fastapi-387914"
  gcp_project_name              = "fastapi"
  gcp_sa_prefix                 = "fastapi"
  gcp_network_project_id        = "fastapi-387914"

  /////   Compute Engine  /////
  gcp_image_project_id          = "ubuntu-os-cloud"
  gcp_bastion_source_image      = "ubuntu-2204-jammy-v20230630"
  gcp_bastion_macine_type       = "e2-medium"
  gcp_enable_shielded_vm        = true
  gcp_shielded_instance_config  = {
    enable_secure_boot          = false,
    enable_vtpm                 = true,
    enable_integrity_monitoring = true
  }

  /////   GKE Prod ENV   /////
  gke_version_channel                 = "STABLE"
  gke_version_prefix                  = "1.27"
  #gke_ip_range_pods                   = "${local.global_env.locals.gcp_node_subnet_name}-${local.gcp_project_id}-${local.env}-pods"
  #gke_ip_range_services               = "${local.global_env.locals.gcp_node_subnet_name}-${local.gcp_project_id}-${local.env}-svcs"
  gke_http_load_balancing             = false
  gke_network_policy                  = true
  gke_horizontal_pod_autoscaling      = true
  gke_filestore_csi_driver            = false
  gke_enable_private_endpoint         = true
  gke_enable_private_nodes            = true
  gke_regional                        = true
  gke_logging_enabled_components      = ["SYSTEM_COMPONENTS"]
  gke_ip_masq_link_local              = true
  gke_configure_ip_masq               = false
  gke_default_max_pods_per_node       = 32
  gke_create_service_account          = false
  gke_remove_default_node_pool        = true
  gke_enable_shielded_nodes           = true
  gke_initial_node_count              = 0
  gke_machine_type                    = "e2-standard-4"
  gke_gce_pd_csi_driver               = true
  gke_deploy_using_private_endpoint   = true
  gke_release_channel                 = "UNSPECIFIED"
  gke_deletion_protection             = false
  gke_ip_range_pods_name              = "${local.env}-gke-ip-pods"
  gke_ip_range_services_name          = "${local.env}-gke-ip-services"
  gke_master_authorized_networks  = [
    {
      cidr_block                  = "${local.global_env.locals.gcp_node_subnet_cidr}"
      display_name                = "${local.gcp_project_id}-network-shared-ic-1-subnet-${local.env}"
    }
  ]

  /////   Services Accounts   /////
  gcp_sa_roles  = [
    "${local.gcp_project_id}=>roles/viewer",
    "${local.gcp_project_id}=>roles/storage.admin",
    "${local.gcp_project_id}=>roles/storage.objectViewer",
    "${local.gcp_project_id}=>roles/compute.networkAdmin",
    "${local.gcp_project_id}=>roles/compute.securityAdmin",
    "${local.gcp_project_id}=>roles/compute.storageAdmin",
    "${local.gcp_project_id}=>roles/compute.osAdminLogin",
    "${local.gcp_project_id}=>roles/compute.serviceAgent",
    "${local.gcp_project_id}=>roles/container.serviceAgent",
    "${local.gcp_project_id}=>roles/container.clusterAdmin",
    "${local.gcp_project_id}=>roles/container.admin",
    "${local.gcp_project_id}=>roles/secretmanager.admin",
    "${local.gcp_project_id}=>roles/file.editor",
    "${local.gcp_project_id}=>roles/cloudkms.admin",
    "${local.gcp_project_id}=>roles/cloudsql.admin",
    "${local.gcp_project_id}=>roles/monitoring.metricWriter",
    "${local.gcp_project_id}=>roles/monitoring.viewer",
    "${local.gcp_project_id}=>roles/logging.logWriter",
    "${local.gcp_project_id}=>roles/logging.configWriter",
  ]

  /////   GCP API Services   /////
  gcp_api_services  = [
    "cloudkms.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "container.googleapis.com",
    "servicenetworking.googleapis.com",
    "dns.googleapis.com",
    "networkmanagement.googleapis.com",
    "cloudapis.googleapis.com",
    "firestore.googleapis.com",
    "file.googleapis.com",
    "iam.googleapis.com",
    "iap.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "secretmanager.googleapis.com",
    "servicemanagement.googleapis.com",
    "serviceusage.googleapis.com",
    "sql-component.googleapis.com",
    "sqladmin.googleapis.com",
    "stackdriver.googleapis.com",
    "storage-component.googleapis.com",
    "storage.googleapis.com",
  ]

  /////   Firewall Ruels   /////
  gcp_firewall_policy_description     = "firewall policy ${local.gcp_project_name} ${local.env}"
  gcp_firewall_policy_rules           = [
    //{
    //  priority       = "10"
    //  direction      = "INGRESS"
    //  action         = "allow"
    //  rule_name      = "allow-internal"
    //  description    = "allow-internal"
    //  enable_logging = true
    //  match = {
    //    src_ip_ranges            = ["172.0.0.0/8"]
    //    layer4_configs = [
    //      {
    //        ip_protocol = "tcp"
    //        ports       = ["0-65535"]
    //      },
    //      {
    //        ip_protocol = "udp"
    //        ports       = ["0-65535"]
    //      },
    //    ]
    //  }
    //},
    {
      priority       = "100"
      direction      = "INGRESS"
      action         = "allow"
      rule_name      = "ssh_connection"
      description    = "open ssh connection"
      enable_logging = true
      match = {
        src_ip_ranges            = ["35.235.240.0/20"]
        layer4_configs = [
          {
            ip_protocol = "tcp"
            ports       = ["22"]
          },
        ]
      }
    },
    //{
    //  priority       = "200"
    //  direction      = "INGRESS"
    //  action         = "allow"
    //  rule_name      = "icmp_connection"
    //  description    = "open icmp connection"
    //  enable_logging = true
    //  match = {
    //    src_ip_ranges            = ["0.0.0.0/0"]
    //    layer4_configs = [
    //      {
    //        ip_protocol = "icmp"
    //      },
    //    ]
    //  }
    //},
    //{
    //  priority       = "300"
    //  direction      = "INGRESS"
    //  action         = "allow"
    //  rule_name      = "https_connection"
    //  description    = "open https connection"
    //  enable_logging = true
    //  match = {
    //    src_ip_ranges            = ["0.0.0.0/0"]
    //    layer4_configs = [
    //      {
    //        ip_protocol = "all"
    //        #ports       = ["443"]
    //      },
    //    ]
    //  }
    //},

    //{
    //  priority       = "2100"
    //  direction      = "EGRESS"
    //  action         = "allow"
    //  rule_name      = "https_connection"
    //  description    = "open https connection"
    //  enable_logging = true
    //  match = {
    //    dest_ip_ranges           = ["0.0.0.0/0"]
    //    layer4_configs = [
    //      {
    //        ip_protocol = "all"
    //      },
    //    ]
    //  }
    //},
  ]


  /////   VPC Routes   /////
  gcp_vpc_routes = [
    {
            name                   = "egress-internet-${local.gcp_project_name}-${local.env}"
            description            = "route through IGW to access internet"
            destination_range      = "0.0.0.0/0"
            tags                   = "egress-inet"
            next_hop_internet      = "true"
        },
  ]


  /////   GCP Cloud SQL (postgresql)   /////
  gcp_cloud_sql_disk_size                     =  40
  gcp_cloud_sql_database_version              = "POSTGRES_15"
  gcp_cloud_sql_db_name                       = "fastapi"
  gcp_cloud_sql_machine_type                  = "db-n1-standard-1"
  gcp_cloud_sql_ip_configuration_require_ssl  = false
  gcp_cloud_sql_ip_configuration_ipv4_enabled = false
  gcp_cloud_sql_database_flags                = [
  ]


  /////   Helm Chart   /////
  argocd_chart_name                   = "argo-cd"
  argocd_chart_version                = "5.45.0"
  argocd_chart_repository             = "https://argoproj.github.io/argo-helm/"
  argocd_values_file_path             = "values.yaml"

  eso_chart_name                   = "external-secrets"
  eso_chart_version                = "0.9.10"
  eso_chart_repository             = "https://charts.external-secrets.io/"
  eso_values_file_path             = "values.yaml"


}