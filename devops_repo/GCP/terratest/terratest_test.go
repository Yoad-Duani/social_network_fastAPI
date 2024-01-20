package test

import (
	"fmt"
	"os"
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
)

func TestTerragruntExample(t *testing.T) {
	terraformDirENV := os.Getenv("TERRAFORM_DIR_ENV")

	if terraformDirENV == "" {
		terraformDirENV = "_tests" // Default value
	}

	terraformDirPATH := fmt.Sprintf("../tg-modules/%s/gcp-vpc", terraformDirENV)

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir:    terraformDirPATH,
		TerraformBinary: "terragrunt",
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.Apply(t, terraformOptions)

	// output := terraform.Output(t, terraformOptions, "output")
	// assert.Equal(t, "one input another input", output)
}
