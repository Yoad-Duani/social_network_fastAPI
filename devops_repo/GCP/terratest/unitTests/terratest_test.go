package unittests

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
)

var terragruntDirEnv string
var region string = "me-west1"

func TestCreateVPCandSUbnetes(t *testing.T) {

	terragruntDirEnv := os.Getenv("TERRAFORM_DIR_ENV")

	if terragruntDirEnv == "" {
		terragruntDirEnv = "_tests" // Default value
	}

	terragruntDirPathVpc := fmt.Sprintf("../../tg-modules/%s/gcp-vpc", terragruntDirEnv)
	terragruntDirPathSubnetes := fmt.Sprintf("../../tg-modules/%s/gcp-subnets", terragruntDirEnv)
	terragruntDirPathApiServicesGCP := fmt.Sprintf("../../tg-modules/%s/gcp-project-services", terragruntDirEnv)
	terragruntDirPathServiceAccount := fmt.Sprintf("../../tg-modules/%s/gcp-service-accounts", terragruntDirEnv)

	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, terragruntDirPathVpc))
	defer terraform.Destroy(t, terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)

	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, terragruntDirPathSubnetes, terragruntOptionsVpc))
	defer terraform.Destroy(t, terragruntOptionsSubnetes)
	terraform.InitAndApply(t, terragruntOptionsSubnetes)

	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, terragruntDirPathApiServicesGCP))
	defer terraform.Destroy(t, terragruntOptionsApiServicesGCP)
	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)

	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, terragruntDirPathServiceAccount))
	defer terraform.Destroy(t, terragruntOptionsServiceAccount)
	terraform.InitAndApply(t, terragruntOptionsServiceAccount)

	// output := terraform.Output(t, terraformOptions, "output")
	// assert.Equal(t, "one input another input", output)
}

func configVPC(t *testing.T, terragruntDirPathVpc string) *terraform.Options {
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathVpc,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": vpcName,
		},
	}
}

func configSubnetes(t *testing.T, terragruntDirPathSubnetes string, terragruntOptionsVpc *terraform.Options) *terraform.Options {
	network_name_output := terraform.Output(t, terragruntOptionsVpc, "network_name")
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)

	return &terraform.Options{
		TerraformDir:    terragruntDirPathSubnetes,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": network_name_output,
			"subnets": []map[string]interface{}{
				{
					"subnet_name":           fmt.Sprintf("subnet-test-general-%s", uniqueIdLower),
					"subnet_ip":             "172.20.10.0/24",
					"subnet_region":         region,
					"subnet_private_access": "true",
					"subnet_flow_logs":      "false",
					"description":           "test subnet general purpose",
				},
				{
					"subnet_name":           fmt.Sprintf("subnet-test-gke-%s", uniqueIdLower),
					"subnet_ip":             "172.20.11.0/24",
					"subnet_region":         region,
					"subnet_private_access": "true",
					"subnet_flow_logs":      "false",
					"description":           "test subnet gke purpose",
				}
			},
			"secondary_ranges": map[string]interface{}{
				fmt.Sprintf("subnet-test-gke-%s", uniqueIdLower): []map[string]interface{}{
					{
						"range_name":    fmt.Sprintf("test-gke-ip-pods-%s", uniqueIdLower),
						"ip_cidr_range": "172.21.0.0/16",
					},
					{
						"range_name":    fmt.Sprintf("test-gke-ip-services-%s", uniqueIdLower),
						"ip_cidr_range": "172.22.0.0/16"
					},
				}
			}
		},
	}
}

func configApiServicesGCP(t *testing.T, terragruntDirPathApiServicesGCP string) *terraform.Options {
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathApiServicesGCP,
		TerraformBinary: "terragrunt",
	}
}

func configServiceAccount(t *testing.T, terragruntDirPathServiceAccount string) *terraform.Options {
	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	return &terraform.Options{
		TerraformDir:    terragruntDirPathServiceAccount,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"names": []string{fmt.Sprintf("project-sa-%s", uniqueIdLower), fmt.Sprintf("terraform-sa-%s", uniqueIdLower)},
		},
	}
}