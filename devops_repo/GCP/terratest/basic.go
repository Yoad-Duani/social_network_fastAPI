package test_terrgrunt

// import (
// 	"testing"

// 	"github.com/gruntwork-io/terratest/modules/terraform"
// )

// func BasicConfCreate(t *testing.T, configPath *DirPathConfig) {
// 	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, configPath.TerragruntDirPathApiServicesGCP))
// 	terraform.InitAndApply(t, terragruntOptionsApiServicesGCP)
// 	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, configPath.TerragruntDirPathServiceAccount))
// 	terraform.InitAndApply(t, terragruntOptionsServiceAccount)
// }

// func BasicConfDelete(t *testing.T, configPath *DirPathConfig) {
// 	terragruntOptionsApiServicesGCP := terraform.WithDefaultRetryableErrors(t, configApiServicesGCP(t, configPath.TerragruntDirPathApiServicesGCP))
// 	defer terraform.Destroy(t, terragruntOptionsApiServicesGCP)
// 	terragruntOptionsServiceAccount := terraform.WithDefaultRetryableErrors(t, configServiceAccount(t, configPath.TerragruntDirPathServiceAccount))
// 	defer terraform.Destroy(t, terragruntOptionsServiceAccount)
// }
