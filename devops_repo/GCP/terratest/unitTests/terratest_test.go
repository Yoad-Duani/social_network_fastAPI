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

func TestCreateVPCandSUbnetes(t *testing.T) {

	terragruntDirEnv := os.Getenv("TERRAFORM_DIR_ENV")

	if terragruntDirEnv == "" {
		terragruntDirEnv = "_tests" // Default value
	}

	terragruntDirPathVpc := fmt.Sprintf("../tg-modules/%s/gcp-vpc", terragruntDirEnv)
	terragruntDirPathSubnetes := fmt.Sprintf("../tg-modules/%s/gcp-subnets", terragruntDirEnv)

	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, terragruntDirPathVpc))
	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, terragruntDirPathSubnetes, terragruntOptionsVpc))

	defer terraform.Destroy(t, terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)

	defer terraform.Destroy(t, terragruntOptionsSubnetes)
	terraform.InitAndApply(t, terragruntOptionsSubnetes)

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
	return &terraform.Options{
		TerraformDir:    terragruntDirPathSubnetes,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": network_name_output,
		},
	}
}
