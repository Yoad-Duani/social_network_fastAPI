package test_terrgrunt

// import (
// 	"fmt"
// 	"os"
// 	"strconv"
// 	"testing"
// )

// // var region string = "me-west1"
// // var terragruntDirEnv = os.Getenv("TERRAFORM_DIR_ENV")

// func main() {

// 	var t *testing.T
// 	unitTestsEnabledStr := os.Getenv("UNIT_TESTS_ENABLED")
// 	integrationTestEnabledStr := os.Getenv("INTEGRATION_TESTS_ENABLED")
// 	fullDeployTestEnabledStr := os.Getenv("FULL_DEPLOY_TEST_ENABLED")

// 	unitTestsEnabled, err := strconv.ParseBool(unitTestsEnabledStr)
// 	if err != nil {
// 		fmt.Printf("Bad input for env %s, should be true or false. ", "UNIT_TESTS_ENABLED")
// 		panic(err)
// 	}

// 	integrationTestEnabled, err := strconv.ParseBool(integrationTestEnabledStr)
// 	if err != nil {
// 		fmt.Printf("Bad input for env %s, should be true or false. ", "INTEGRATION_TESTS_ENABLED")
// 		panic(err)
// 	}

// 	fullDeployTestEnabled, err := strconv.ParseBool(fullDeployTestEnabledStr)
// 	if err != nil {
// 		fmt.Printf("Bad input for env %s, should be true or false. ", "FULL_DEPLOY_TEST_ENABLED")
// 		panic(err)
// 	}

// 	configPath := NewDirPathConfig()
// 	BasicConfCreate(t, configPath)

// 	if unitTestsEnabled {
// 		fmt.Printf("some data")
// 	}

// 	if integrationTestEnabled {
// 		fmt.Printf("some data")
// 	}

// 	if fullDeployTestEnabled {
// 		fmt.Printf("some data")
// 	}

// 	// if terragruntDirEnv == "" {
// 	// 	terragruntDirEnv = "_tests" // Default value
// 	// }

// 	// var terragruntDirPathVpc = fmt.Sprintf("../../tg-modules/%s/gcp-vpc", terragruntDirEnv)
// 	// var terragruntDirPathSubnetes = fmt.Sprintf("../../tg-modules/%s/gcp-subnets", terragruntDirEnv)
// 	// // var terragruntDirPathApiServicesGCP := fmt.Sprintf("../../tg-modules/%s/gcp-project-services", terragruntDirEnv)
// 	// var terragruntDirPathServiceAccount = fmt.Sprintf("../../tg-modules/%s/gcp-service-accounts", terragruntDirEnv)
// 	// var terragruntDirPathRoutes = fmt.Sprintf("../../tg-modules/%s/gcp-routes", terragruntDirEnv)
// 	// var terragruntDirPathFirewallPolicy = fmt.Sprintf("../../tg-modules/%s/gcp-firewall-policy", terragruntDirEnv)
// 	// var terragruntDirPathCloudRouterNat = fmt.Sprintf("../../tg-modules/%s/gcp-cloud-router-nat", terragruntDirEnv)
// 	// var terragruntDirPathGkeVersion = fmt.Sprintf("../../tg-modules/%s/gcp-gke-version", terragruntDirEnv)
// 	// var terragruntDirPathGKE = fmt.Sprintf("../../tg-modules/%s/gcp-gke", terragruntDirEnv)

// 	// TestCreateVPCandSUbnetes(t, terragruntDirPathVpc)

// }

// // func TestCreateVPCandSUbnetes(t *testing.T, terragruntDirPathVpc string) {
// // 	terragruntOptionsVpc := terraform.WithDefaultRetryableErrors(t, configVPC(t, terragruntDirPathVpc))
// // 	defer terraform.Destroy(t, terragruntOptionsVpc)
// // 	terraform.InitAndApply(t, terragruntOptionsVpc)
// // }

// // func TestUnitTest(t *testing.T, terragruntDirPathVpc string) {

// // }

// // func TestIntegrationTest(t *testing.T, terragruntDirPathVpc string) {

// // }

// // func fullDeployTest(t *testing.T, terragruntDirPathVpc string) {

// // }
