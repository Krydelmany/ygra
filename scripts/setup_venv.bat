@echo off
setlocal enabledelayedexpansion
set PY=py -3.12

%PY% -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install

echo.
echo ✅ Ambiente pronto!
echo Ative depois com: .venv\Scripts\activate
