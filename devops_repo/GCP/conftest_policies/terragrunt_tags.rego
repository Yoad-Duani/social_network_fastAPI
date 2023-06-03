package main

import data.gcp.compute.firewalls
import data.gcp.compute.networks

# Ensure VPC has a valid network name
violation[msg] {
    vpc := networks[_]
    not vpc.name
    msg := sprintf("VPC resource is missing network name.")
}

# # Ensure VPC has at least one firewall rule
# violation[msg] {
#     vpc := networks[_]
#     not firewalls[_].network == vpc.self_link
#     msg := sprintf("VPC resource does not have any firewall rules.")
# }



