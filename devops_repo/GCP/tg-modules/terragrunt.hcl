# ------------------------------------------------------------------------------
# Global Terragrunt Configuration
# ------------------------------------------------------------------------------

locals {
    account_vars        = read_terragrunt_config(find_in_parent_folders("account.hcl"))
}