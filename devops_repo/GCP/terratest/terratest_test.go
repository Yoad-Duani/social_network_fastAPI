package test_terrgrunt

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
)

var MyConfig = NewConfig()

// TestDeployBasic is deploy service accounts with the required permissions and enable gcp APIs for all tets.
func TestDeployBasic(t *testing.T) {
	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, MyConfig.TerragruntDirPathApiServicesGCP))
	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)

	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, MyConfig.TerragruntDirPathServiceAccount))
	terraform.InitAndApply(t, terragruntOptionsServiceAccount)
}

// func TestUnitTestsVPC(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	// network_id := terraform.Output(t, terragruntOptionsVpc, "network_id")
// 	// validateVPC(t, network_id)
// }

// func TestUnitTestsSubnets(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)
// }

// func TestUnitTestsVpcRoutes(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)

// 	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfig.TerragruntDirPathRoutes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsRoutes)
// 	terraform.InitAndApply(t, terragruntOptionsRoutes)

// 	// TODO: Add check for routes (access outside)
// }

// func TestUnitTestsFirewallPolicy(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)

// 	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfig.TerragruntDirPathRoutes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsRoutes)
// 	terraform.InitAndApply(t, terragruntOptionsRoutes)

// 	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, MyConfig.TerragruntDirPathFirewallPolicy, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsFirewallPolicy)
// 	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)

// 	// TODO: Add check for firewall access
// }

// func TestUnitTestsCloudRouterNat(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)

// 	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfig.TerragruntDirPathRoutes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsRoutes)
// 	terraform.InitAndApply(t, terragruntOptionsRoutes)

// 	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, MyConfig.TerragruntDirPathFirewallPolicy, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsFirewallPolicy)
// 	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)

// 	terragruntOptionsCloudRouterNat := terraform.WithDefaultRetryableErrors(t, configCloudRouterNat(t, MyConfig.TerragruntDirPathCloudRouterNat, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsCloudRouterNat)
// 	terraform.InitAndApply(t, terragruntOptionsCloudRouterNat)

// 	// TODO: Add check for Cloud Router Nat access
// }

func TestUnitTestsGKE(t *testing.T) {
	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
	defer terraform.Destroy(t, terragruntOptionsVpc)
	terraform.InitAndApply(t, terragruntOptionsVpc)

	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
	defer terraform.Destroy(t, terragruntOptionsSubnetes)
	terraform.InitAndApply(t, terragruntOptionsSubnetes)

	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfig.TerragruntDirPathRoutes, terragruntOptionsVpc))
	defer terraform.Destroy(t, terragruntOptionsRoutes)
	terraform.InitAndApply(t, terragruntOptionsRoutes)

	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, MyConfig.TerragruntDirPathFirewallPolicy, terragruntOptionsVpc))
	defer terraform.Destroy(t, terragruntOptionsFirewallPolicy)
	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)

	terragruntOptionsCloudRouterNat := terraform.WithDefaultRetryableErrors(t, configCloudRouterNat(t, MyConfig.TerragruntDirPathCloudRouterNat, terragruntOptionsVpc, MyConfig.Region))
	defer terraform.Destroy(t, terragruntOptionsCloudRouterNat)
	terraform.InitAndApply(t, terragruntOptionsCloudRouterNat)

	terragruntOptionsGkeVersion := terraform.WithDefaultRetryableErrors(t, configGkeVersion(t, MyConfig.TerragruntDirPathGkeVersion, MyConfig.Region))
	defer terraform.Destroy(t, terragruntOptionsGkeVersion)
	terraform.InitAndApply(t, terragruntOptionsGkeVersion)

	terragruntOptionsGKE := terraform.WithDefaultRetryableErrors(t, configGKE(t, MyConfig.TerragruntDirPathGKE, terragruntOptionsGkeVersion, terragruntOptionsVpc, terragruntOptionsSubnetes, MyConfig.Region))
	defer terraform.Destroy(t, terragruntOptionsGKE)
	terraform.InitAndApply(t, terragruntOptionsGKE)

	// TODO: Add check for GKE Cluster
}

// func TestUnitTestsBastionVM(t *testing.T) {
// 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, MyConfig.TerragruntDirPathVpc))
// 	defer terraform.Destroy(t, terragruntOptionsVpc)
// 	terraform.InitAndApply(t, terragruntOptionsVpc)

// 	terragruntOptionsSubnetes := terraform.WithDefaultRetryableErrors(t, configSubnetes(t, MyConfig.TerragruntDirPathSubnetes, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsSubnetes)
// 	terraform.InitAndApply(t, terragruntOptionsSubnetes)

// 	terragruntOptionsRoutes := terraform.WithDefaultRetryableErrors(t, configRoutes(t, MyConfig.TerragruntDirPathRoutes, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsRoutes)
// 	terraform.InitAndApply(t, terragruntOptionsRoutes)

// 	terragruntOptionsFirewallPolicy := terraform.WithDefaultRetryableErrors(t, configFirewallPolicy(t, MyConfig.TerragruntDirPathFirewallPolicy, terragruntOptionsVpc))
// 	defer terraform.Destroy(t, terragruntOptionsFirewallPolicy)
// 	terraform.InitAndApply(t, terragruntOptionsFirewallPolicy)

// 	terragruntOptionsCloudRouterNat := terraform.WithDefaultRetryableErrors(t, configCloudRouterNat(t, MyConfig.TerragruntDirPathCloudRouterNat, terragruntOptionsVpc, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsCloudRouterNat)
// 	terraform.InitAndApply(t, terragruntOptionsCloudRouterNat)

// 	terragruntOptionsInstanceTemplateBastion := terraform.WithDefaultRetryableErrors(t, configInstanceTemplateBastion(t, MyConfig.TerragruntDirPathInstanceTemplateBastion, MyConfig.Region))
// 	defer terraform.Destroy(t, terragruntOptionsInstanceTemplateBastion)
// 	terraform.InitAndApply(t, terragruntOptionsInstanceTemplateBastion)

// }
