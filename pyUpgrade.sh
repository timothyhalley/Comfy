#!/bin/zsh
pyenv install --list | grep 3.12
# pyenv install --list | grep 3.13
# pyenv install --list | grep 3.14   


pyenv install 3.12.7
pyenv global 3.12.7


#rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install maturin

