# Before You Deploy

## What we are going to deploy?

We will use terragrunt to deploy a complete infrastructure to run a gke cluster, this includes:

- VPC and Subnets
- Sarvice Accounts and GCP APIs
- Compute Instance and Instance Template

## Cost

> ⚠️ **_NOTE:_**  Even if you use the Free Tier of GCP, some services will cost money, 
                   **pay attention to the section on shutdown the environment.**