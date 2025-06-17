VERSION=$1
wget https://github.com/tmrotz/li-playwright/releases/download/$VERSION/li_playwright-$VERSION-py3-none-any.whl ~/li_playwright-$VERSION-py3-none-any.whl
pip install --upgrade ~/li_playwright-$VERSION-py3-none-any.whl
