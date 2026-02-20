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

## Segurança
- Nunca commitar tokens/credenciais
- Usar `.env` local (baseado no `.env.example`)
