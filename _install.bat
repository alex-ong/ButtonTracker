:: install pipx, enables `poetry.exe` to be in a virtualenv lol
python -m pip install pipx
pipx install poetry
:: poetry can't find python3.8 beacuse its called python.exe. rough.
poetry env use C:/Python38/python.exe
poetry install