package test_terrgrunt

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
)

type Config struct {
	Region                                   string
	RegionZones                              string
	DefaultZone                              string
	Env                                      string
	ProjectID                                string
	ProjectName                              string
	NetworkProjectID                         string
	TerragruntDirEnv                         string
	TerragruntDirPathVpc                     string
	TerragruntDirPathSubnetes                string
	TerragruntDirPathServiceAccount          string
	TerragruntDirPathApiServicesGCP          string
	TerragruntDirPathRoutes                  string
	TerragruntDirPathFirewallPolicy          string
	TerragruntDirPathCloudRouterNat          string
	TerragruntDirPathGkeVersion              string
	TerragruntDirPathGKE                     string
	TerragruntDirPathInstanceTemplateBastion string
	TerragruntDirPathInstanceBastion         string
}

func NewConfig() *Config {
	terragruntDirEnv := os.Getenv("TERRAFORM_DIR_ENV")
	if terragruntDirEnv == "" {
		terragruntDirEnv = "_tests" // Default value
	}
	return &Config{
		Region:                                   "me-west1",
		TerragruntDirEnv:                         terragruntDirEnv,
		TerragruntDirPathVpc:                     fmt.Sprintf("%s/gcp-vpc", terragruntDirEnv),
		TerragruntDirPathSubnetes:                fmt.Sprintf("../tg-modules/%s/gcp-subnets", terragruntDirEnv),
		TerragruntDirPathServiceAccount:          fmt.Sprintf("../tg-modules/%s/gcp-service-accounts", terragruntDirEnv),
		TerragruntDirPathApiServicesGCP:          fmt.Sprintf("../tg-modules/%s/gcp-project-services", terragruntDirEnv),
		TerragruntDirPathRoutes:                  fmt.Sprintf("../tg-modules/%s/gcp-routes", terragruntDirEnv),
		TerragruntDirPathFirewallPolicy:          fmt.Sprintf("../tg-modules/%s/gcp-firewall-policy", terragruntDirEnv),
		TerragruntDirPathCloudRouterNat:          fmt.Sprintf("../tg-modules/%s/gcp-cloud-router-nat", terragruntDirEnv),
		TerragruntDirPathGkeVersion:              fmt.Sprintf("../tg-modules/%s/gcp-gke-version", terragruntDirEnv),
		TerragruntDirPathGKE:                     fmt.Sprintf("../tg-modules/%s/gcp-gke", terragruntDirEnv),
		TerragruntDirPathInstanceTemplateBastion: fmt.Sprintf("../tg-modules/%s/gcp-instance-template-bastion", terragruntDirEnv),
		TerragruntDirPathInstanceBastion:         fmt.Sprintf("../tg-modules/%s/gcp-instance-bastion", terragruntDirEnv),
	}
}

func GetTerraformOptionsForFormatTests(t *testing.T, terragruntDirEnv string) *terraform.Options {
	terragruntFolder := fmt.Sprintf("../tg-modules/%s", terragruntDirEnv)

	maxTerraformRetries := 3
	sleepBetweenTerraformRetries := 5 * time.Second
	retryableTerraformErrors := map[string]string{
		".*unable to verify signature.*":             "Failed to retrieve plugin due to transient network error.",
		".*unable to verify checksum.*":              "Failed to retrieve plugin due to transient network error.",
		".*no provider exists with the given name.*": "Failed to retrieve plugin due to transient network error.",
		".*registry service is unreachable.*":        "Failed to retrieve plugin due to transient network error.",
		".*connection reset by peer.*":               "Failed to retrieve plugin due to transient network error.",
	}

	terraformOptions := &terraform.Options{
		TerraformDir:             terragruntFolder,
		TerraformBinary:          "terragrunt",
		Vars:                     map[string]interface{}{},
		NoColor:                  true,
		RetryableTerraformErrors: retryableTerraformErrors,
		MaxRetries:               maxTerraformRetries,
		TimeBetweenRetries:       sleepBetweenTerraformRetries,
	}
	return terraformOptions
}

// func parseEnvHCL(filename string) (map[string]interface{}, error) {
// 	envConfig := make(map[string]interface{})

// 	// Read the content of the HCL file
// 	content, err := os.ReadFile(filename)
// 	if err != nil {
// 		return nil, err
// 	}

// 	// Parse the HCL content
// 	hclContent := string(content)
// 	node, err := parser.Parse([]byte(hclContent))
// 	if err != nil {
// 		return nil, err
// 	}

// 	// Visit the AST to extract values
// 	ast.Walk(node.Node, func(n ast.Node) bool {
// 		switch n := n.(type) {
// 		case *ast.ObjectItem:
// 			key := strings.TrimSpace(n.Keys[0].Token.Value().(string))
// 			value := strings.TrimSpace(n.Val.(*ast.StringLit).Token.Value().(string))
// 			envConfig[key] = value
// 		}
// 		return true
// 	})

// 	return envConfig, nil
// }

func configApiServicesGCP(t *testing.T, terragruntDirPathApiServicesGCP string) *terraform.Options {
	return &terraform.Options{
		TerraformDir:    terragruntDirPathApiServicesGCP,
		TerraformBinary: "terragrunt",
	}
}

func configServiceAccount(t *testing.T, terragruntDirPathServiceAccount string) *terraform.Options {
	// uniqueId := random.UniqueId()
	// uniqueIdLower := strings.ToLower(uniqueId)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathServiceAccount,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"names":  []string{"project-sa", "terraform-sa"},
			"prefix": "",
		},
	}
}

func configVPC(t *testing.T, terragruntDirPathVpc string) *terraform.Options {
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)
	options := GetTerraformOptionsForFormatTests(t, terragruntDirPathVpc)

	options.Vars["network_name"] = vpcName
	return options

	// return &terraform.Options{
	// 	TerraformDir:    terragruntDirPathVpc,
	// 	TerraformBinary: "terragrunt",
	// 	Vars: map[string]interface{}{
	// 		"network_name": vpcName,
	// 	},
	// }
}

// func configVPC(t *testing.T, terragruntDirPathVpc string) *terraform.Options {
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)
// 	return &terraform.Options{
// 		TerraformDir:             terragruntDirPathVpc,
// 		TerraformBinary:          "terragrunt",
// 		MaxRetries:               3,
// 		TimeBetweenRetries:       3 * time.Second,
// 		RetryableTerraformErrors: map[string]string{},
// 		Vars: map[string]interface{}{
// 			"network_name": vpcName,
// 		},
// 	}
// }

func configSubnetes(t *testing.T, terragruntDirPathSubnetes string, terragruntOptionsVpc *terraform.Options, region string) *terraform.Options {
	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
	// uniqueId := random.UniqueId()
	// uniqueIdLower := strings.ToLower(uniqueId)

	return &terraform.Options{
		TerraformDir:    terragruntDirPathSubnetes,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": network_name_output,
			"subnets": []map[string]interface{}{
				// {
				// 	"subnet_name":           fmt.Sprintf("subnet-test-general-%s", uniqueIdLower),
				// 	"subnet_ip":             "172.20.10.0/24",
				// 	"subnet_region":         region,
				// 	"subnet_private_access": "true",
				// 	"subnet_flow_logs":      "false",
				// 	"description":           "test subnet general purpose",
				// },
				// {
				// 	"subnet_name":           fmt.Sprintf("subnet-test-gke-%s", uniqueIdLower),
				// 	"subnet_ip":             "172.20.11.0/24",
				// 	"subnet_region":         region,
				// 	"subnet_private_access": "true",
				// 	"subnet_flow_logs":      "false",
				// 	"description":           "test subnet gke purpose",
				// },
				{
					"subnet_name":           "subnet-general",
					"subnet_ip":             "172.20.10.0/24",
					"subnet_region":         region,
					"subnet_private_access": "true",
					"subnet_flow_logs":      "false",
					"description":           "test subnet general purpose",
				},
				{
					"subnet_name":           "subnet-gke",
					"subnet_ip":             "172.20.11.0/24",
					"subnet_region":         region,
					"subnet_private_access": "true",
					"subnet_flow_logs":      "false",
					"description":           "test subnet gke purpose",
				},
			},
			"secondary_ranges": map[string]interface{}{
				"subnet-gke": []map[string]interface{}{
					{
						"range_name":    "gke-ip-pods",
						"ip_cidr_range": "172.21.0.0/16",
					},
					{
						"range_name":    "gke-ip-services",
						"ip_cidr_range": "172.22.0.0/16",
					},
				},
			},
		},
	}
}

func configRoutes(t *testing.T, terragruntDirPathRoutes string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)

	return &terraform.Options{
		TerraformDir:    terragruntDirPathRoutes,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": network_name_output,
			"routes": []map[string]interface{}{
				{
					"name":              fmt.Sprintf("egress-internet-test-%s", uniqueIdLower),
					"description":       "route through IGW to access internet",
					"destination_range": "0.0.0.0/0",
					"tags":              "egress-inet",
					"next_hop_internet": "true",
				},
			},
		},
	}
}

func configFirewallPolicy(t *testing.T, terragruntDirPathFirewallPolicy string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
	network_id_output := terraform.Output(t, terragruntOptionsVpc, "network_id")
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	firewallPolicyName := fmt.Sprintf("firewall-policy-%s", uniqueIdLower)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathFirewallPolicy,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"policy_name": firewallPolicyName,
			"target_vpcs": []string{network_id_output},
		},
	}
}

func configCloudRouterNat(t *testing.T, terragruntDirPathFirewallPolicy string, terragruntOptionsVpc *terraform.Options, region string) *terraform.Options {
	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	natName := fmt.Sprintf("nat-router-%s", uniqueIdLower)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathFirewallPolicy,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"name":    natName,
			"network": network_name_output,
			"region":  region,
			"nats": []map[string]interface{}{
				{
					"name": fmt.Sprintf("%s-nat-%s", network_name_output, uniqueIdLower),
				},
			},
		},
	}
}

func configGkeVersion(t *testing.T, terragruntDirPathGkeVersion string, region string) *terraform.Options {
	return &terraform.Options{
		TerraformDir:    terragruntDirPathGkeVersion,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"gcp_region": region,
			"env":        "test",
		},
	}
}

func configGKE(t *testing.T, terragruntDirPathGKE string, terragruntOptionsGkeVersion *terraform.Options, terragruntOptionsVpc *terraform.Options, terragruntOptionsSubnetes *terraform.Options, region string) *terraform.Options {
	// available_zones_names_output := terraform.Output(t, terragruntOptionsGkeVersion, "available_zones_names")
	gke_version_output := terraform.Output(t, terragruntOptionsGkeVersion, "version")
	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
	// network_id_output := terraform.Output(t, terragruntOptionsVpc, "network_id")
	// subnets_name_output := terraform.Output(t, terragruntOptionsSubnetes, "subnets")
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)

	return &terraform.Options{
		TerraformDir:    terragruntDirPathGKE,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"name":               fmt.Sprintf("test-gke-%s", uniqueIdLower),
			"region":             region,
			"kubernetes_version": gke_version_output,
			"network":            network_name_output,
			"subnetwork":         "subnet-gke",
			"ip_range_pods":      "gke-ip-pods",
			"ip_range_services":  "gke-ip-services",
			"master_authorized_networks": []map[string]interface{}{
				{
					"cidr_block":   "172.20.10.0/24",
					"display_name": "gke-master-authorized-network-subnet-general",
				},
			},
			"service_account": "project-sa@test-deploy-392912.iam.gserviceaccount.com",
			"node_pools": []map[string]interface{}{
				{
					"name":               "management",
					"machine_type":       "e2-standard-2",
					"min_count":          1,
					"max_count":          1,
					"local_ssd_count":    0,
					"disk_size_gb":       80,
					"disk_type":          "pd-standard",
					"image_type":         "COS_CONTAINERD",
					"auto_repair":        true,
					"auto_upgrade":       false,
					"service_account":    "project-sa@test-deploy-392912.iam.gserviceaccount.com",
					"preemptible":        false,
					"initial_node_count": 1,
					"enable_secure_boot": true,
				},
				{
					"name":               "services",
					"machine_type":       "e2-standard-2",
					"min_count":          1,
					"max_count":          2,
					"local_ssd_count":    0,
					"disk_size_gb":       80,
					"disk_type":          "pd-standard",
					"image_type":         "COS_CONTAINERD",
					"auto_repair":        true,
					"auto_upgrade":       false,
					"service_account":    "project-sa@test-deploy-392912.iam.gserviceaccount.com",
					"preemptible":        false,
					"initial_node_count": 1,
					"enable_secure_boot": true,
				},
				{
					"name":               "stateful",
					"machine_type":       "e2-standard-2",
					"min_count":          1,
					"max_count":          1,
					"local_ssd_count":    0,
					"disk_size_gb":       80,
					"disk_type":          "pd-standard",
					"image_type":         "COS_CONTAINERD",
					"auto_repair":        true,
					"auto_upgrade":       false,
					"service_account":    "project-sa@test-deploy-392912.iam.gserviceaccount.com",
					"preemptible":        false,
					"initial_node_count": 1,
					"enable_secure_boot": true,
				},
			},
		},
	}
}

func configInstanceTemplateBastion(t *testing.T, terragruntDirPathInstanceTemplateBastion string, region string) *terraform.Options {
	return &terraform.Options{
		TerraformDir:    terragruntDirPathInstanceTemplateBastion,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"region":          region,
			"name_prefix":     "test-bastion",
			"subnetwork":      "subnet-general",
			"service_account": "project-sa@test-deploy-392912.iam.gserviceaccount.com",
		},
	}
}

func configBastionVM(t *testing.T, TerragruntDirPathInstanceBastion string, terragruntDirPathInstanceTemplateBastion *terraform.Options, region string, zone string) *terraform.Options {
	instance_template := terraform.Output(t, terragruntDirPathInstanceTemplateBastion, "self_link")
	return &terraform.Options{
		TerraformDir:    TerragruntDirPathInstanceBastion,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"region":            region,
			"zone":              zone,
			"instance_template": instance_template,
		},
	}
}
