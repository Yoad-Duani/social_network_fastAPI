package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

var MyConfigStages = NewConfig()

func deployVpcStage() {
	var t *testing.T
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfigStages.TerragruntDirPathVpc))
	test_structure.SaveTerraformOptions(t, "/tmp", terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)
}

func cleanVpcStage() {
	var t *testing.T
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp")
	terraform.Destroy(t, terragruntOptionsVpc)
}
