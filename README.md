# Example Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.


# Installation
python3 -m venv venv
. venv/bin/activate
pip install -e .[dev]
playwright install && playwright install-deps

# Run
python -m message -c message

# Wheel
## Create
python -m build

## Install/Upgrade
1. sudo apt install python3.12-venv xclip
1. python3 -m venv venv
1. sudo apt install python3-pip
1. . venv/bin/activate
1. WHEEL_V=0.0.2
1. wget https://github.com/tmrotz/li-playwright/releases/download/"$WHEEL_V"/li_playwright-"$WHEEL_V"-py3-none-any.whl
1. pip install --upgrade li_playwright-"$WHEEL_V"-py3-none-any.whl
1. playwright install && playwright install-deps
1. touch config.ini
1. mkdir states
1. cp config.ini down down down

## Run
python -m message -c message
