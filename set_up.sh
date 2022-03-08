#!/bin/bash

echo "Checking Git"
git_version=$(git --version)
if [[ "${git_version}" != *"git version"* ]]; then
  echo "Installing Git"
  sudo apt install git
fi

echo "Git clone to /opt/dns_update/"
cd /opt/
sudo git clone https://github.com/etidahouse/dns_update.git dns_update

echo "Installing Python3.8 ?[O/n]"
read py_install

if [[ "${py_install,,}" == "o" ]]; then
  echo "Checking Python version"
  py_version=$(python3 -V);
  if [[ "${py_version}" == *"3.8"* ]]; then
    echo "Python 3.8 already installed"
    python3 -m pip install --upgrade pip
    pip install pydantic
  else
    echo "Installing Python 3.8"
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.8
    pip install pydantic
  fi
fi

echo "Installing bind9 ?[O/n]"
read bind9_install
if [[ "${bind9_install,,}" == "o" ]]; then
  echo "Checking bind9"
  bind9_version=$(dpkg -l bind9)
  if [[ "${bind9_version}" != *"BIND"* ]]; then
    echo "Installing bind9"
    sudo apt install bind9
  fi
fi

echo "Create systemd dns_update service ?[O/n]"
read dns_update_service
if [[ "${dns_update_service,,}" == "o" ]]; then
  cd /etc/systemd/system/
  sudo curl https://raw.githubusercontent.com/etidahouse/dns_update/main/files/dns_update.service -o dns_update.service
  sudo systemctl enable dns_update
fi

echo "---------------------------------------------------------------------------------"
echo "The setup is complete."
echo "---------------------------------------------------------------------------------"
echo "Now you need to edit the config.json file located: /opt/dns_update/config.json"
echo "You can also edit the logging.ini file located at /opt/dns_update/files/logging.ini"
echo "Finally, don't forget to edit your zone file: /opt/dns_update/files/zone.template"
echo "Don't forget to read the readme for more information."
