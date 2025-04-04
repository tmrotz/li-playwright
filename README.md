# Example Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.



# Installation
python3 -m venv venv
. venv/bin/activate
pip install -e .[dev]

# Create Wheel
python -m build

# Wheel
## Install/Upgrade
sudo apt install python3.12-venv
python3 -m venv venv
sudo apt install python3-pip
. venv/bin/activate
WHEEL_V=0.0.2
wget https://github.com/tmrotz/li-playwright/releases/download/"$WHEEL_V"/li_playwright-"$WHEEL_V"-py3-none-any.whl
pip install --upgrade li_playwright-0.0.2-py3-none-any.whl

## Run
asdf

