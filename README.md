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
gh release create 1.2.1 dist/li_playwright-1.2.1-py3-none-any.whl

## Run
python -m tgl -c scrape
