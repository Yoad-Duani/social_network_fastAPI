package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

// "github.com/gruntwork-io/terratest/modules/testing"

var MyConfigStages = NewConfig()

// Deploy
func deployVpcStage(t *testing.T) {
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfigStages.TerragruntDirPathVpc))
	test_structure.SaveTerraformOptions(t, "/tmp/vpc", terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)
}

func deploySubnetsStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfigStages.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfigStages.Region))
	test_structure.SaveTerraformOptions(t, "/tmp/subnets", terragruntOptionsSubnetes)
	terraform.InitAndApply(t, terragruntOptionsSubnetes)
}

func deployRoutesStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfigStages.TerragruntDirPathRoutes, terragruntOptionsVpc))
	test_structure.SaveTerraformOptions(t, "/tmp/routes", terragruntOptionsRoutes)
	terraform.InitAndApply(t, terragruntOptionsRoutes)
}

func deployFirewallPolicyStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, MyConfigStages.TerragruntDirPathFirewallPolicy, terragruntOptionsVpc))
	test_structure.SaveTerraformOptions(t, "/tmp/firewall-policy", terragruntOptionsFirewallPolicy)
	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)
}

func deployCloudRouterNatStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terragruntOptionsCloudRouterNat := terraform.WithDefaultRetryableErrors(t, configCloudRouterNat(t, MyConfigStages.TerragruntDirPathCloudRouterNat, terragruntOptionsVpc, MyConfigStages.Region))
	test_structure.SaveTerraformOptions(t, "/tmp/cloud-router-nat", terragruntOptionsCloudRouterNat)
	terraform.InitAndApply(t, terragruntOptionsCloudRouterNat)
}

func deployGkeVersionStage(t *testing.T) {
	terragruntOptionsGkeVersion := terraform.WithDefaultRetryableErrors(t, configGkeVersion(t, MyConfigStages.TerragruntDirPathGkeVersion, MyConfigStages.Region))
	test_structure.SaveTerraformOptions(t, "/tmp/gke-version", terragruntOptionsGkeVersion)
	terraform.InitAndApply(t, terragruntOptionsGkeVersion)
}

func deployGkeStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terragruntOptionsGkeVersion := test_structure.LoadTerraformOptions(t, "/tmp/gke-version")
	terragruntOptionsSubnetes := test_structure.LoadTerraformOptions(t, "/tmp/subnets")
	terragruntOptionsGKE := terraform.WithDefaultRetryableErrors(t, configGKE(t, MyConfigStages.TerragruntDirPathGKE, terragruntOptionsGkeVersion, terragruntOptionsVpc, terragruntOptionsSubnetes, MyConfigStages.Region))
	test_structure.SaveTerraformOptions(t, "/tmp/gke", terragruntOptionsGKE)
	terraform.InitAndApply(t, terragruntOptionsGKE)
}

// Clean
func cleanVpcStage(t *testing.T) {
	terragruntOptionsVpc := test_structure.LoadTerraformOptions(t, "/tmp/vpc")
	terraform.Destroy(t, terragruntOptionsVpc)
}

func cleanSubnetsStage(t *testing.T) {
	terragruntOptionsSubnetes := test_structure.LoadTerraformOptions(t, "/tmp/subnets")
	terraform.Destroy(t, terragruntOptionsSubnetes)
}

func cleanRoutesStage(t *testing.T) {
	terragruntOptionsRoutes := test_structure.LoadTerraformOptions(t, "/tmp/routes")
	terraform.Destroy(t, terragruntOptionsRoutes)
}

func cleanFirewallPolicyStage(t *testing.T) {
	terragruntOptionsFirewallPolicy := test_structure.LoadTerraformOptions(t, "/tmp/firewall-policy")
	terraform.Destroy(t, terragruntOptionsFirewallPolicy)
}

func cleanCloudRouterNatStage(t *testing.T) {
	terragruntOptionsCloudRouterNat := test_structure.LoadTerraformOptions(t, "/tmp/cloud-router-nat")
	terraform.Destroy(t, terragruntOptionsCloudRouterNat)
}

func cleanGkeVersionStage(t *testing.T) {
	terragruntOptionsGkeVersion := test_structure.LoadTerraformOptions(t, "/tmp/gke-version")
	terraform.Destroy(t, terragruntOptionsGkeVersion)
}

func cleanGkeStage(t *testing.T) {
	terragruntOptionsGKE := test_structure.LoadTerraformOptions(t, "/tmp/gke")
	terraform.Destroy(t, terragruntOptionsGKE)
}
