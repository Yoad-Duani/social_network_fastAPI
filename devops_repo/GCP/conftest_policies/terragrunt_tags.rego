package main


deny[msg] {
    not input.terraform.source
    msg = "Terraform block missing `source`"
}

deny[msg] {
    not contains(input.terraform.source, input.include.env.locals.google_tf_source_module)
    msg = sprintf("Terraform block `source` does not contain the expected module %s", [input.include.env.locals.google_tf_source_module])
}

deny[msg] {
    not contains(input.terraform.source, input.include.env.locals.google_tf_source_provider)
    msg = sprintf("Terraform block `source` does not contain the expected provider %s", [input.include.env.locals.google_tf_source_provider])
}

# deny[msg] {
#     not contains(input.terraform.source, "/vpc?ref=v7.0.0")
#     msg = "Terraform block `source` does not contain the expected reference"
# }

# import data.gcp.compute.firewalls
# import data.gcp.compute.networks

# # Ensure VPC has a valid network name
# deny[msg] {
#     input.vpc := networks[_]
#     not input.vpc.name
#     msg := sprintf("VPC resource %s is missing network name.", [input.vpc.name])
# }

# # Ensure VPC has at least one firewall rule
# violation[msg] {
#     vpc := networks[_]
#     not firewalls[_].network == vpc.self_link
#     msg := sprintf("VPC resource does not have any firewall rules.")
# }



