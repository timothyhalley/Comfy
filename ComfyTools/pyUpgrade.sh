#!/bin/zsh
pyenv install --list | grep 3.12
# pyenv install --list | grep 3.13
# pyenv install --list | grep 3.14   


pyenv install 3.12.7
pyenv global 3.12.7

brew install openssl readline sqlite3 xz zlib


#rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install maturin

#---------------------------


### To upgrade Python using pyenv from version 3.12.7 to 3.12.8 (or the latest subversion), you can follow these steps:

### Update pyenv: First, make sure your pyenv is up to date.

cd ~/.pyenv
git pull

### Install the new Python version: Use pyenv to install the desired Python version.

pyenv install 3.12.8

### Set the new version: Set the newly installed version as the global or local Python version.

pyenv global 3.12.8
# or for a specific project
### pyenv local 3.12.8
Verify the installation: Check that the new version is being used.

python --version