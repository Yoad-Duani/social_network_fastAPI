package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
)

// import (
// 	"fmt"
// 	"os"
// 	"strings"
// 	"testing"

// 	"github.com/gruntwork-io/terratest/modules/random"
// 	"github.com/gruntwork-io/terratest/modules/terraform"
// )

// var terragruntDirEnv string
// var region string = "me-west1"

// func TestCreateVPCandSUbnetes(t *testing.T) {

// 	terragruntDirEnv := os.Getenv("TERRAFORM_DIR_ENV")

// 	if terragruntDirEnv == "" {
// 		terragruntDirEnv = "_tests" // Default value
// 	}

var MyConfig = NewConfig()

// 	terragruntDirPathVpc := fmt.Sprintf("../../tg-modules/%s/gcp-vpc", terragruntDirEnv)
// 	terragruntDirPathSubnetes := fmt.Sprintf("../../tg-modules/%s/gcp-subnets", terragruntDirEnv)
// 	// terragruntDirPathApiServicesGCP := fmt.Sprintf("../../tg-modules/%s/gcp-project-services", terragruntDirEnv)
// 	terragruntDirPathServiceAccount := fmt.Sprintf("../../tg-modules/%s/gcp-service-accounts", terragruntDirEnv)
// 	terragruntDirPathRoutes := fmt.Sprintf("../../tg-modules/%s/gcp-routes", terragruntDirEnv)
// 	terragruntDirPathFirewallPolicy := fmt.Sprintf("../../tg-modules/%s/gcp-firewall-policy", terragruntDirEnv)
// 	terragruntDirPathCloudRouterNat := fmt.Sprintf("../../tg-modules/%s/gcp-cloud-router-nat", terragruntDirEnv)
// 	terragruntDirPathGkeVersion := fmt.Sprintf("../../tg-modules/%s/gcp-gke-version", terragruntDirEnv)
// 	terragruntDirPathGKE := fmt.Sprintf("../../tg-modules/%s/gcp-gke", terragruntDirEnv)

func TestDeployBasic(t *testing.T) {
	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, MyConfig.TerragruntDirPathApiServicesGCP))
	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)

	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, MyConfig.TerragruntDirPathServiceAccount))
	terraform.InitAndApply(t, terragruntOptionsServiceAccount)
}

func TestUnitTestsVPC(t *testing.T) {
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
	defer terraform.Destroy(t, terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)
}

func TestUnitTestsVpcSubnets(t *testing.T) {
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
	defer terraform.Destroy(t, terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)

	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
	defer terraform.Destroy(t, terragruntOptionsSubnetes)
	terraform.InitAndApply(t, terragruntOptionsSubnetes)
}

// func BasicConfCreate(t *testing.T, config Config) {
// 	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, config.TerragruntDirPathApiServicesGCP))
// 	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)
// 	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, config.TerragruntDirPathServiceAccount))
// 	terraform.InitAndApply(t, terragruntOptionsServiceAccount)
// }

// func BasicConfDelete(t *testing.T, config Config) {
// 	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, config.TerragruntDirPathApiServicesGCP))
// 	defer terraform.Destroy(t, terragruntOptionsApiServicesGCP)
// 	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, config.TerragruntDirPathServiceAccount))
// 	defer terraform.Destroy(t, terragruntOptionsServiceAccount)
// }

// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, terragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, terragruntDirPathSubnetes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)

// 	// terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, terragruntDirPathApiServicesGCP))
// 	// defer terraform.Destroy(t, terragruntOptionsApiServicesGCP)
// 	// terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)

// 	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, terragruntDirPathServiceAccount))
// 	defer terraform.Destroy(t, terragruntOptionsServiceAccount)
// 	terraform.InitAndApply(t, terragruntOptionsServiceAccount)

// 	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, terragruntDirPathRoutes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsRoutes)
// 	terraform.InitAndApply(t, terragruntOptionsRoutes)

// 	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, terragruntDirPathFirewallPolicy, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsFirewallPolicy)
// 	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)

// 	terragruntOptionsCloudRouterNat := terraform.WithDefaultRetryableErrors(t, configCloudRouterNat(t, terragruntDirPathCloudRouterNat, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsCloudRouterNat)
// 	terraform.InitAndApply(t, terragruntOptionsCloudRouterNat)

// 	terragruntOptionsGkeVersion := terraform.WithDefaultRetryableErrors(t, configGkeVersion(t, terragruntDirPathGkeVersion))
// 	defer terraform.Destroy(t, terragruntOptionsGkeVersion)
// 	terraform.InitAndApply(t, terragruntOptionsGkeVersion)

// 	terragruntOptionsGKE := terraform.WithDefaultRetryableErrors(t, configGKE(t, terragruntDirPathGKE, terragruntOptionsGkeVersion, terragruntOptionsVpc, terragruntOptionsSubnetes, terragruntOptionsServiceAccount))
// 	defer terraform.Destroy(t, terragruntOptionsGKE)
// 	terraform.InitAndApply(t, terragruntOptionsGKE)

// 	// output := terraform.Output(t, terraformOptions, "output")
// 	// assert.Equal(t, "one input another input", output)
// }

// func configVPC(t *testing.T, terragruntDirPathVpc string) *terraform.Options {
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathVpc,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"network_name": vpcName,
// 		},
// 	}
// }

// func configSubnetes(t *testing.T, terragruntDirPathSubnetes string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
// 	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)

// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathSubnetes,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"network_name": network_name_output,
// 			"subnets": []map[string]interface{}{
// 				{
// 					"subnet_name":           fmt.Sprintf("subnet-test-general-%s", uniqueIdLower),
// 					"subnet_ip":             "172.20.10.0/24",
// 					"subnet_region":         region,
// 					"subnet_private_access": "true",
// 					"subnet_flow_logs":      "false",
// 					"description":           "test subnet general purpose",
// 				},
// 				{
// 					"subnet_name":           fmt.Sprintf("subnet-test-gke-%s", uniqueIdLower),
// 					"subnet_ip":             "172.20.11.0/24",
// 					"subnet_region":         region,
// 					"subnet_private_access": "true",
// 					"subnet_flow_logs":      "false",
// 					"description":           "test subnet gke purpose",
// 				},
// 			},
// 			"secondary_ranges": map[string]interface{}{
// 				fmt.Sprintf("subnet-test-gke-%s", uniqueIdLower): []map[string]interface{}{
// 					{
// 						"range_name":    fmt.Sprintf("test-gke-ip-pods-%s", uniqueIdLower),
// 						"ip_cidr_range": "172.21.0.0/16",
// 					},
// 					{
// 						"range_name":    fmt.Sprintf("test-gke-ip-services-%s", uniqueIdLower),
// 						"ip_cidr_range": "172.22.0.0/16",
// 					},
// 				},
// 			},
// 		},
// 	}
// }

// // func configApiServicesGCP(t *testing.T, terragruntDirPathApiServicesGCP string) *terraform.Options {
// // 	return &terraform.Options{
// // 		TerraformDir:    terragruntDirPathApiServicesGCP,
// // 		TerraformBinary: "terragrunt",
// // 	}
// // }

// func configServiceAccount(t *testing.T, terragruntDirPathServiceAccount string) *terraform.Options {
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathServiceAccount,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"names": []string{fmt.Sprintf("proj-sa-%s", uniqueIdLower), fmt.Sprintf("tf-sa-%s", uniqueIdLower)},
// 		},
// 	}
// }

// func configRoutes(t *testing.T, terragruntDirPathRoutes string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
// 	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)

// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathRoutes,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"network_name": network_name_output,
// 			"routes": []map[string]interface{}{
// 				{
// 					"name":              fmt.Sprintf("egress-internet-test-%s", uniqueIdLower),
// 					"description":       "route through IGW to access internet",
// 					"destination_range": "0.0.0.0/0",
// 					"tags":              "egress-inet",
// 					"next_hop_internet": "true",
// 				},
// 			},
// 		},
// 	}
// }

// func configFirewallPolicy(t *testing.T, terragruntDirPathFirewallPolicy string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
// 	network_id_output := terraform.Output(t, terragruntOptionsVpc, "network_id")
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	firewallPolicyName := fmt.Sprintf("firewall-policy-%s", uniqueIdLower)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathFirewallPolicy,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"policy_name": firewallPolicyName,
// 			"target_vpcs": []string{network_id_output},
// 		},
// 	}
// }

// func configCloudRouterNat(t *testing.T, terragruntDirPathFirewallPolicy string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
// 	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	natName := fmt.Sprintf("nat-router-%s", uniqueIdLower)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathFirewallPolicy,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"name":    natName,
// 			"network": network_name_output,
// 			"region":  region,
// 			"nats": []map[string]interface{}{
// 				{
// 					"name": fmt.Sprintf("%s-nat-%s", network_name_output, uniqueIdLower),
// 				},
// 			},
// 		},
// 	}
// }

// func configGkeVersion(t *testing.T, terragruntDirPathGkeVersion string) *terraform.Options {
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathGkeVersion,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"gcp_region": region,
// 			"env":        "test",
// 		},
// 	}
// }

// func configGKE(t *testing.T, terragruntDirPathGKE string, terragruntOptionsGkeVersion *terraform.Options, terragruntOptionsVpc *terraform.Options, terragruntOptionsSubnetes *terraform.Options, terragruntOptionsServiceAccount *terraform.Options) *terraform.Options {
// 	available_zones_names_output := terraform.Output(t, terragruntOptionsGkeVersion, "available_zones_names")
// 	gke_version_output := terraform.Output(t, terragruntOptionsGkeVersion, "version")
// 	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
// 	network_id_output := terraform.Output(t, terragruntOptionsVpc, "network_id")
// 	subnets_name_output := terraform.Output(t, terragruntOptionsSubnetes, "subnets")
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)

// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathGKE,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"name":               fmt.Sprintf("test-gke-%s", uniqueIdLower),
// 			"region":             region,
// 			"kubernetes_version": gke_version_output,
// 			"network":            network_name_output,
// 			"subnetwork":         subnets_name_output,
// 		},
// 	}
// }

// type Config struct {
// 	Region                          string
// 	RegionZones                     string
// 	DefaultZone                     string
// 	Env                             string
// 	ProjectID                       string
// 	ProjectName                     string
// 	NetworkProjectID                string
// 	TerragruntDirEnv                string
// 	TerragruntDirPathVpc            string
// 	TerragruntDirPathSubnetes       string
// 	TerragruntDirPathServiceAccount string
// 	TerragruntDirPathApiServicesGCP string
// 	TerragruntDirPathRoutes         string
// 	TerragruntDirPathFirewallPolicy string
// 	TerragruntDirPathCloudRouterNat string
// 	TerragruntDirPathGkeVersion     string
// 	TerragruntDirPathGKE            string
// }

// func NewConfig() *Config {
// 	terragruntDirEnv := os.Getenv("TERRAFORM_DIR_ENV")
// 	if terragruntDirEnv == "" {
// 		terragruntDirEnv = "_tests" // Default value
// 	}
// 	return &Config{
// 		Region:                          "me-west1",
// 		TerragruntDirEnv:                terragruntDirEnv,
// 		TerragruntDirPathVpc:            fmt.Sprintf("../tg-modules/%s/gcp-vpc", terragruntDirEnv),
// 		TerragruntDirPathSubnetes:       fmt.Sprintf("../tg-modules/%s/gcp-subnets", terragruntDirEnv),
// 		TerragruntDirPathServiceAccount: fmt.Sprintf("../tg-modules/%s/gcp-service-accounts", terragruntDirEnv),
// 		TerragruntDirPathApiServicesGCP: fmt.Sprintf("../tg-modules/%s/gcp-project-services", terragruntDirEnv),
// 		TerragruntDirPathRoutes:         fmt.Sprintf("../tg-modules/%s/gcp-routes", terragruntDirEnv),
// 		TerragruntDirPathFirewallPolicy: fmt.Sprintf("../tg-modules/%s/gcp-firewall-policy", terragruntDirEnv),
// 		TerragruntDirPathCloudRouterNat: fmt.Sprintf("../tg-modules/%s/gcp-cloud-router-nat", terragruntDirEnv),
// 		TerragruntDirPathGkeVersion:     fmt.Sprintf("../tg-modules/%s/gcp-gke-version", terragruntDirEnv),
// 		TerragruntDirPathGKE:            fmt.Sprintf("../tg-modules/%s/gcp-gke", terragruntDirEnv),
// 	}
// }

// func configVPC(t *testing.T, terragruntDirPathVpc string) *terraform.Options {
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathVpc,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"network_name": vpcName,
// 		},
// 	}
// }

// func configApiServicesGCP(t *testing.T, terragruntDirPathApiServicesGCP string) *terraform.Options {
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathApiServicesGCP,
// 		TerraformBinary: "terragrunt",
// 	}
// }

// func configServiceAccount(t *testing.T, terragruntDirPathServiceAccount string) *terraform.Options {
// 	uniqueId := random.UniqueId()
// 	uniqueIdLower := strings.ToLower(uniqueId)
// 	return &terraform.Options{
// 		TerraformDir:    terragruntDirPathServiceAccount,
// 		TerraformBinary: "terragrunt",
// 		Vars: map[string]interface{}{
// 			"names": []string{fmt.Sprintf("proj-sa-%s", uniqueIdLower), fmt.Sprintf("tf-sa-%s", uniqueIdLower)},
// 		},
// 	}
// }
