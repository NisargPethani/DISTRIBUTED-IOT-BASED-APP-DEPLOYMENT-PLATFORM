#!/bin/bash
# sudo apt-get update
# sudo apt-get install ca-certificates curl apt-transport-https lsb-release gnupg

echo "##################### Installing prerequisites #######################################"
printf "\n\n"

echo "#### Installing Azure CLI ####"
printf "\n\n"
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

printf "\n\n"
echo "#### Installing Docker Machine ####"
printf "\n\n"
base=https://github.com/docker/machine/releases/download/v0.16.0 \
  && curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine \
  && sudo mv /tmp/docker-machine /usr/local/bin/docker-machine \
  && chmod +x /usr/local/bin/docker-machine

printf "\n\n"
echo "#### Installing gnome-terminal ####"
printf "\n\n"
sudo apt update
sudo apt install gnome-terminal

