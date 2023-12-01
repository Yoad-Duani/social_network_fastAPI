#!/usr/bin/env bash

#### Install ZSH
sudo apt update
sudo apt -y upgrade
sudo apt -y install zsh

# Additional packages
sudo apt -y install git \
         unzip \
         wget \
         python3 \
         python3-venv \
         nfs-common \
         openjdk-11-jdk \
         dnsutils \
         net-tools \
         python3-pip

VENV_PATH=~/virtualenv
python3.9 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

# Symbolic links for SELinux
cd ${VENV_PATH}/lib/python3.9/site-packages/
sudo ln -s /usr/lib/python3/dist-packages/selinux
sudo ln -s /usr/lib/python3/dist-packages/_selinux.cpython-39-x86_64-linux-gnu.so

# Upgrade pip and install required Python packages
pip install --upgrade pip
pip install --upgrade cython rust setuptools-rust cryptography setuptools google-api-python-client jmespath
pip install ansible==8.1.0

source ${VENV_PATH}/bin/deactivate

#### Terraform Installation
TERRAFORM_VERSION="1.5.2"
if [[ -f /usr/local/bin/terraform ]]; then
    echo "/usr/local/bin/terraform exists. doing nothing"
else
    echo "--- Installing Terraform(${TERRAFORM_VERSION}) ---"
    curl -L https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
    unzip /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /tmp/
    sudo mv /tmp/terraform /usr/local/bin/terraform
    sudo chmod 755 /usr/local/bin/terraform
    sudo rm -rf /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
fi

#### Terragrunt Installation
TERRAGRUNT_VERSION="v0.45.11"
if [[ -f /usr/local/bin/terragrunt ]]; then
    echo "/usr/local/bin/terragrunt exists. doing nothing"
else
    echo "--- Installing Terragrunt(${TERRAGRUNT_VERSION}) ---"
    wget https://github.com/gruntwork-io/terragrunt/releases/download/$TERRAGRUNT_VERSION/terragrunt_linux_amd64
    sudo mv terragrunt_linux_amd64 /usr/local/bin/terragrunt
    sudo chmod 755 /usr/local/bin/terragrunt
    sudo rm terragrunt_linux_amd64
fi

#### Add more tools binaries
sudo apt -y install jq
wget https://github.com/simeji/jid/releases/download/v0.7.6/jid_linux_amd64.zip
unzip jid_linux_amd64.zip
sudo mv jid /usr/local/bin

#### Install kubectl + Helm
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

sudo apt -y install apt-transport-https
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-add-repository "deb https://baltocdn.com/helm/stable/debian/ all main"
sudo apt -y update
sudo apt -y install helm

#### Krew install
OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
KREW="krew-${OS}_${ARCH}" &&
curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
tar zxvf "${KREW}.tar.gz" &&
bash ./"${KREW}" install krew
kubectl krew install iexec
kubectl krew install ctx
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >>~/.zshrc

#### Install argocd-cli
wget https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo mv argocd-linux-amd64 /usr/local/bin/argocd
sudo chmod +x /usr/local/bin/argocd

##### Useful bash Aliases
cat << EOF >> ~/.bashrc
alias tg='terragrunt'
alias tga='terragrunt run-all'

alias kk='kubectl get po -w -o wide'
alias k='kubectl'
EOF