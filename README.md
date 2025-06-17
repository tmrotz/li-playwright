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
python -m tgl -c message

# Wheel
## Create
python -m build

## Run
python -m tgl -c scrape
