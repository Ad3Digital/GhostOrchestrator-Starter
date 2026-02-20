# Ghost Orchestrator Starter

Starter kit para alunos criarem loops de execução com agentes (X -> Y -> Z) usando OpenClaw.

## O que vem pronto
- Orchestrator local (fila de jobs + histórico)
- Dashboard local (kanban + eventos)
- Templates de jobs (conteúdo, tráfego, suporte)
- Scripts de instalação e setup

## Requisitos
- Python 3.10+
- OpenClaw instalado

## Instalação rápida
### Windows
```powershell
./install.ps1
python setup.py
python orchestrator/scripts/tick.py
python dashboard/server.py
```

### Linux/macOS
```bash
chmod +x install.sh
./install.sh
python3 setup.py
python3 orchestrator/scripts/tick.py
python3 dashboard/server.py
```

Abra: `http://127.0.0.1:7071`

## Fluxo recomendado
1. Criar job com `orchestrator/scripts/create_job.py`
2. Rodar tick (manual ou cron)
3. Aprovar/rejeitar jobs em `review`
4. Acompanhar no dashboard

## Publicar no GitHub
1. Criar repo vazio
2. `git init`
3. `git add . && git commit -m "starter v1"`
4. `git branch -M main`
5. `git remote add origin <URL_DO_REPO>`
6. `git push -u origin main`

## Usar com o próprio agente no OpenClaw

Tu pode pedir pro próprio agente importar e configurar o starter no teu PC.

### Passo a passo (comando para o agente)
1. Clonar o repo:
   - `git clone https://github.com/Ad3Digital/GhostOrchestrator-Starter.git`
2. Entrar na pasta do projeto
3. Rodar instalação (`install.ps1` no Windows ou `install.sh` no Linux/macOS)
4. Rodar setup (`python setup.py`)
5. Subir dashboard (`python dashboard/server.py`)

### Exemplo de pedido no OpenClaw
"Julius, clona o repo GhostOrchestrator-Starter, instala as dependências, roda o setup e sobe o dashboard."

## Segurança
- Nunca commitar tokens/credenciais
- Usar `.env` local (baseado no `.env.example`)
