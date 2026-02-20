Write-Host "[Ghost Orchestrator] Instalando dependências..."
python -m pip install --upgrade pip
if (Test-Path "requirements.txt") {
  python -m pip install -r requirements.txt
}
Write-Host "Instalação concluída. Rode: python setup.py"
