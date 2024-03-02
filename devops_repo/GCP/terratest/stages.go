package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

var t *testing.T
var MyConfigStages = NewConfig()

func deployVpcStage() {
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfigStages.TerragruntDirPathVpc))
	test_structure.SaveTerraformOptions(t, "/tmp", terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)
}

func cleanVpcStage() {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp")
	terraform.Destroy(t, terragruntOptionsVpc)
}
