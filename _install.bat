:: install pipx, enables `poetry.exe` to be in a virtualenv lol
python -m pip install pipx
pipx install poetry
:: poetry might not be added to path (rip)
pipx ensurepath
poetry self add poetry-dotenv-plugin
:: poetry can't find python3.8 beacuse its called python.exe. rough.
poetry env use C:/Python311/python.exe
poetry install

@echo off
echo If poetry didn't work, you have to re-open your cmd. sorry mate
@echo on