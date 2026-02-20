#!/usr/bin/env bash
set -e

echo "[Ghost Orchestrator] Instalando dependências..."
python3 -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  python3 -m pip install -r requirements.txt
fi
echo "Instalação concluída. Rode: python3 setup.py"
