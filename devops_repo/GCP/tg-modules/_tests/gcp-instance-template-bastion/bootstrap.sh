#!/usr/bin/env bash
####################
##  Ubuntu setup  ##
####################

ANSIBLE_VERSION="8.1.0"
TERRAFORM_VERSION="1.5.2"
TERRAGRUNT_VERSION="v0.45.11"
VENV_PATH=~/virtualenv

#### Install ZSH
# apt update
sudo apt clean
sudo apt update -y
#sudo apt -y upgrade
#sudo apt -y install zsh

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

python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

# Symbolic links for SELinux
# cd ${VENV_PATH}/lib/python3.9/site-packages/
# sudo ln -s /usr/lib/python3/dist-packages/selinux
# sudo ln -s /usr/lib/python3/dist-packages/_selinux.cpython-39-x86_64-linux-gnu.so

# Upgrade pip and install required Python packages
pip install --upgrade pip
pip install --upgrade cython rust setuptools-rust cryptography setuptools google-api-python-client jmespath
pip install ansible==${ANSIBLE_VERSION}
source ${VENV_PATH}/bin/deactivate

# git clone https://github.com/jotyGill/ezsh.git
# cd ezsh
# ./install.sh -c

#### Terraform Installation
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
(
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    yes | ~/.fzf/install
    sudo apt -y install jq
    wget https://github.com/simeji/jid/releases/download/v0.7.6/jid_linux_amd64.zip
    unzip jid_linux_amd64.zip
    sudo mv jid /usr/local/bin
)

#### Install kubectl + Helm
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

#sudo apt -y install apt-transport-https
#curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
#sudo apt-add-repository "deb https://baltocdn.com/helm/stable/debian/ all main" ###
#sudo apt -y update
#sudo apt -y install helm

curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm


#### Krew install
OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
KREW="krew-${OS}_${ARCH}" &&
curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
tar zxvf "${KREW}.tar.gz" &&
./"${KREW}" install krew
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
kubectl krew install iexec
kubectl krew install ctx
kubectl krew install ns
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >>~/.zshrc

# zsh
git clone https://github.com/jotyGill/ezsh.git
cd ezsh
./install.sh -c
echo "exec zsh" >>~/.bashrc
source ~/.zshrc

#### Install argocd-cli
wget https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo mv argocd-linux-amd64 /usr/local/bin/argocd
sudo chmod +x /usr/local/bin/argocd

##### Useful bash Aliases
cat << EOF >> ~/.zshrc
alias tg='terragrunt'
alias tf='terraform'
alias tga='terragrunt run-all'

alias kk='kubectl get po -w -o wide'
alias k='kubectl'
alias ctx='kubectl ctx'
alias kns='kubectl ns'
EOF