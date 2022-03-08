#!/bin/shell

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

bind9_version=$(dpkg -l bind9)

if [[ "${bind9_version}" != *"BIND"* ]]; then
  echo "Installing bind9"
  sudo apt install bind9
fi
