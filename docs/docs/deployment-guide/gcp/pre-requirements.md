# Pre Requirements

> **_NOTE:_**  The deployment will be based on Linux, all Windows users are recommended to have WSL installed.

## Working Google Cloud SDK

Make sure you have the Google Cloud SDK / gcloud CLI installed and set up on your local machine before proceeding with the deployment:
[Install gcloud cli](https://cloud.google.com/sdk/docs/install)
<br/>

## GCP account / application default credentials

GCP Application Default Credentials are pre-configured credentials that Terraform can use without the need for explicit provider configuration, simplifying the deployment process.
```bash
gcloud auth application-default login
```
you can read more about it here:
[Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-user-cred)

## GCP projects
Create at least two GCP project, we are going to deploy and manage multiple environments using Terragrunt
```bash
gcloud projects create fastapi-prod
```
```bash
gcloud projects create fastapi-preprod
```

## Terraform and Terragrunt

Install Terraform and Terrgrunt, you can use this simple script
> **_NOTE:_**  I'm using terraform 1.5.4, one of the versions before the license changed

create install.sh file, copy and paste  
run the script `./install.sh`

```bash
#!/usr/bin/env bash
#### Terraform Installation:
(
TERRAFORM_VERSION="1.5.4"
if [[ -f /usr/local/bin/terraform ]]; then
    echo  "/usr/local/bin/terraform exist. doing nothing"
else
    echo  "--- Installing Terraform(${TERRAFORM_VERSION}) ---"
    curl -L  https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
    unzip /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip  -d  /tmp/
    sudo mv  /tmp/terraform  /usr/local/bin/terraform
    sudo chmod  755  /usr/local/bin/terraform
    sudo rm  -rf  /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 
fi
)

#### Terragrunt Installation:
(
TERRAGRUNT_VERSION="v0.45.11"
if [[ -f /usr/local/bin/terragrunt ]]; then
    echo  "/usr/local/bin/terragrunt exist. doing nothing"
else
    echo  "--- Installing Terragrunt(${TERRAGRUNT_VERSION}) ---"
    wget https://github.com/gruntwork-io/terragrunt/releases/download/$TERRAGRUNT_VERSION/terragrunt_linux_amd64
    sudo mv  terragrunt_linux_amd64  /usr/local/bin/terragrunt
    sudo chmod  755  /usr/local/bin/terragrunt
    sudo rm  terragrunt_linux_amd64
fi
)
```

## Clone the repository

```bash
git clone https://github.com/Yoad-Duani/social_network_fastAPI.git
```

