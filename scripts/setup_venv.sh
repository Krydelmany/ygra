#!/usr/bin/env bash
set -euo pipefail

PY="python3.12"

if ! command -v $PY &> /dev/null; then
  echo "Python 3.12 não encontrado. Ajuste a variável PY neste script."
  exit 1
fi

$PY -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install

echo
echo "✅ Ambiente pronto!"
echo "Ative com: source .venv/bin/activate"
