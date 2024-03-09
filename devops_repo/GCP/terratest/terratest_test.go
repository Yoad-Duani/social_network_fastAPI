package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

var MyConfig = NewConfig()

// TestDeployBasic is deploy service accounts with the required permissions and enable gcp APIs for all tets.
func TestDeployBasic(t *testing.T) {
	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, MyConfig.TerragruntDirPathApiServicesGCP))
	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)

	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, MyConfig.TerragruntDirPathServiceAccount))
	terraform.InitAndApply(t, terragruntOptionsServiceAccount)
}

func TestUnitTestsGKE(t *testing.T) {
	// t.Parallel()

	// Deploy
	test_structure.RunTestStage(t, "deploy_vpc", func() {
		deployVpcStage(t)
	})

	test_structure.RunTestStage(t, "deploy_subnets", func() {
		deploySubnetsStage(t)
	})

	test_structure.RunTestStage(t, "deploy_routes", func() {
		deployRoutesStage(t)
	})

	test_structure.RunTestStage(t, "deploy_firewall_policy", func() {
		deployFirewallPolicyStage(t)
	})

	test_structure.RunTestStage(t, "deploy_cloud_router_nat", func() {
		deployCloudRouterNatStage(t)
	})

	test_structure.RunTestStage(t, "deploy_gke_version", func() {
		deployGkeVersionStage(t)
	})

	test_structure.RunTestStage(t, "deploy_gke", func() {
		deployGkeStage(t)
	})

	// Validates

	// Clean
	test_structure.RunTestStage(t, "clean_gke", func() {
		cleanGkeStage(t)
	})

	test_structure.RunTestStage(t, "clean_gke_version", func() {
		cleanGkeVersionStage(t)
	})

	test_structure.RunTestStage(t, "clean_cloud_router_nat", func() {
		cleanCloudRouterNatStage(t)
	})

	test_structure.RunTestStage(t, "clean_firewall-policy", func() {
		cleanFirewallPolicyStage(t)
	})

	test_structure.RunTestStage(t, "clean_routes", func() {
		cleanRoutesStage(t)
	})

	test_structure.RunTestStage(t, "clean_subnets", func() {
		cleanSubnetsStage(t)
	})

	test_structure.RunTestStage(t, "clean_vpc", func() {
		cleanVpcStage(t)
	})
}

// func TestUnitTestsBastionVM(t *testing.T) {
// 	// t.Parallel()
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)
// }
