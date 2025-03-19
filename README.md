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

# Install/Upgrade Wheel
pip install --upgrade <path/to/wheel>

