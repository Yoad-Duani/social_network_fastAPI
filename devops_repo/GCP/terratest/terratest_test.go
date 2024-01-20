package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerragruntExample(t *testing.T) {
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir:    "../tg-modules/_tests/gcp-vpc",
		TerraformBinary: "terragrunt",
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.Apply(t, terraformOptions)

	output := terraform.Output(t, terraformOptions, "output")
	assert.Equal(t, "one input another input", output)
}
