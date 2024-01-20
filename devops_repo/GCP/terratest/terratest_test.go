package testvpc

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
)

func TestCreateVPC(t *testing.T) {

	uniqueId := random.UniqueId()
	uniqueIdLower := strings.ToLower(uniqueId)
	vpcName := fmt.Sprintf("vpc-test-%s", uniqueIdLower)

	terraformDirENV := os.Getenv("TERRAFORM_DIR_ENV")

	if terraformDirENV == "" {
		terraformDirENV = "_tests" // Default value
	}

	terraformDirPATH := fmt.Sprintf("../tg-modules/%s/gcp-vpc", terraformDirENV)

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir:    terraformDirPATH,
		TerraformBinary: "terragrunt",
		Vars: map[string]interface{}{
			"network_name": vpcName,
		},
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.Apply(t, terraformOptions)

	// output := terraform.Output(t, terraformOptions, "output")
	// assert.Equal(t, "one input another input", output)
}
