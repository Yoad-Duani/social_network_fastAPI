#!/usr/bin/env bash

#### Install ZSH
sudo dnf clean all
sudo yum -y update
# exec zsh

ANSIBLE_VERSION="8.1.0"

sudo yum check-update
sudo yum -y install git \
         unzip \
         wget \
         python3 \
         virtualenv \
         nfs-utils \
         java-11-openjdk-devel \
         bind-utils \
         net-tools \
         python3-pip
VENV_PATH=~/virtualenv
python3.9 -m venv ${VENV_PATH}
# virtualenv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

cd ${VENV_PATH}lib/python3.6/site-packages/
ln -s /usr/lib64/python3.6/site-packages/selinux
ln -s /usr/lib64/python3.6/site-packages/_selinux.cpython-36m-x86_64-linux-gnu.so

## NOT NEEDED --python3.6 -m venv --system-site-packages ${VENV_PATH}--
pip3 install --upgrade pip
pip3 install --upgrade   cython
pip3 install --upgrade rust setuptools-rust
pip3 install --upgrade cryptography
pip3 install --upgrade setuptools google-api-python-client jmespath
pip3 install ansible==${ANSIBLE_VERSION}

source ${VENV_PATH}/bin/deactivate


#### docker setup (useful for server connect of 1password provider for tg)
# (
# sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
# sudo dnf install docker-ce --nobest -y
# sudo systemctl start docker
# sudo systemctl enable docker
# sudo curl -l "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose
# sudo groupadd docker
# sudo usermod -ag docker $user
# sudo newgrp docker
# )


##### Useful bash Aliases

(
cat << EOF >> ~/.bashrc
alias tg='terragrunt'
alias tga='terragrunt run-all'

alias kk='kubectl get po -w -o wide'
alias k='kubectl'
EOF
)





#### Terraform Installation:
(
TERRAFORM_VERSION="1.5.2"

if [[ -f /usr/local/bin/terraform ]]; then
        echo "/usr/local/bin/terraform exist. doing nothing"
else
  echo "--- Installing Terraform(${TERRAFORM_VERSION}) ---"
  curl -L https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
        unzip /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /tmp/
        sudo mv /tmp/terraform /usr/local/bin/terraform
        sudo chmod 755 /usr/local/bin/terraform
  sudo rm -rf /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip

fi
)

#### Terragrunt Installation:
(
TERRAGRUNT_VERSION="v0.45.11"

if [[ -f /usr/local/bin/terragrunt ]]; then
        echo "/usr/local/bin/terragrunt exist. doing nothing"
else
  echo "--- Installing Terragrunt(${TERRAGRUNT_VERSION}) ---"
        wget https://github.com/gruntwork-io/terragrunt/releases/download/$TERRAGRUNT_VERSION/terragrunt_linux_amd64
        sudo mv terragrunt_linux_amd64 /usr/local/bin/terragrunt
        sudo chmod 755 /usr/local/bin/terragrunt
  sudo rm terragrunt_linux_amd64
fi
)


#### Add more tools binaries
(
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
# ~/.fzf/install

sudo yum install -y jq
wget https://github.com/simeji/jid/releases/download/v0.7.6/jid_linux_amd64.zip
unzip jid_linux_amd64.zip
sudo mv jid /usr/local/bin
)


#### Install kubcectl + Helm

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
(
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
sudo yum install -y kubectl
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

echo 'alias k=kubectl' >>~/.zshrc
echo 'ssh-keyscan gitrepo.xlaxiata.id | argocd cert add-ssh --batch' >> ~/.zshrc
echo "source <(kubectl completion zsh)" >>~/.zshrc

sudo yum install -y google-cloud-sdk-gke-gcloud-auth-plugin
)

#### Krew install


(
# OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
KREW="krew-${OS}_${ARCH}" &&
curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
tar zxvf "${KREW}.tar.gz" &&
bash ./"${KREW}" install krew
kubectl krew install iexec
kubectl krew install ctx
)
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >>~/.zshrc
# Then add noce plugins
(
#### Install oh-my-zsh & kube aliases
sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo yum install -y neovim python3-neovim

curl -sLf https://spacevim.org/install.sh | bash
git clone https://github.com/jotyGill/ezsh
cd ezsh
./install.sh -c        # only run with '-c' the first time, running multiple times will duplicate history entries
echo "exec zsh" >> ~/.bashrc
source ~/.zshrc
echo 'compdef __start_kubectl k' >>~/.zshrc

)


## Gimmie .p10k.zsh !!
(
# git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ~/powerlevel10k
# echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
# echo 'POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=false' >>! ~/.zshrc
# git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
# git clone https://github.com/hanjunlee/terragrunt-oh-my-zsh-plugin ~/.oh-my-zsh/custom/plugins/terragrunt
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
# git clone https://github.com/zsh-users/zsh-completions ~/.oh-my-zsh/custom/plugins/zsh-completions
# git clone https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git "$ZSH_CUSTOM/plugins/autoswitch_virtualenv"
wget  curl -o ~/.p10k.zsh -LO https://gist.githubusercontent.com/levmichael3/a5f22181a9f1e806b318ebed66fc753f/raw/09ef7a1fb4ce14f04a39ce2cd5a5bb558732dece/.p10k.zsh
# echo '''plugins=(git keychain gpg-agent autoswitch_virtualenv  zsh-autosuggestions zsh-completions terraform  git-auto-fetch gcloud git-auto-fetch gcloud zsh-syntax-highlighting git-auto-fetch docker ssh-agent  history kubectl fzf terragrunt ansible)'''>> ~/.zshrc
wget https://raw.githubusercontent.com/ahmetb/kubectl-aliases/master/.kubectl_aliases -O ~/.kubectl_aliases
bash-completion
cat << EOF >> ~/.config/ezsh/ezshrc.zsh
plugins+=( git-auto-fetch gcloud zsh-syntax-highlighting ssh-agent )
[ -f ~/.kubectl_aliases ] && source ~/.kubectl_aliases
compdef __start_kubectl k
# get zsh complete kubectl
source <(kubectl completion zsh)
alias kubectl=kubecolor
# make completion work with kubecolor

compdef kubecolor=kubectl
autoload -Uz compinit
compinit
source ~/.p10k.zsh
EOF
source ~/.zshrc
# (I will have different p10k for each env with context colors!)
)



#### Install argocd-cli
(
wget https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo mv argocd-linux-amd64 /usr/local/bin/argocd
sudo chmod +x /usr/local/bin/argocd
)

##### Add  ~ VERY ~ lazy shell functions



cat << EOF >> ~/.zshrc
function toolazy() {
  local SLOTH
  VENV() {
      VENV_PATH=~/virtualenv ; source ${VENV_PATH}/bin/activate
      cd ~/xl-config/GCP/uat/ansible # change to your env
  }

  ANSIBLE_PULL() {
      cd ~/ansible-roles ; git pull ; cd -
  }

  LOKI_ME() {
    kubectl port-forward svc/loki -n monitoring 3100:3100 &
    export LOKI_ADDR="http://localhost:3100"
    export LOKI_USERNAME=$(kubectl -n monitoring get secret monitor-grafana -o jsonpath="{.data.admin-user}" | base64 -d; echo)
    export LOKI_PASSWORD=$(kubectl -n monitoring get secret monitor-grafana -o jsonpath="{.data.admin-password}" | base64 -d; echo)
  }

  ARGO() {
    export ARGOCD_OPTS='--port-forward-namespace argocd'
    kubectl port-forward svc/argo-argocd-server -n argocd 8080:443 &
    export ARGO_PASS=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo)
    argocd login --plaintext --port-forward --port-forward-namespace argocd --insecure --username admin --password "${ARGO_PASS}"
  }

SLOTH=`printf '%s\n' VENV ANSIBLE_PULL LOKI_ME ARGO  | fzf`

if [[ -n \$SLOTH ]]
then
   \$SLOTH
fi
}
EOF







