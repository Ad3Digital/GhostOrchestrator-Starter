import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cfg_path = ROOT / 'orchestrator' / 'configs' / 'student.config.json'
cfg_path.parent.mkdir(parents=True, exist_ok=True)

print('=== Ghost Orchestrator Setup ===')
owner = input('Nome do aluno: ').strip() or 'Aluno'
channel = input('Canal principal (telegram/whatsapp) [telegram]: ').strip() or 'telegram'

cfg = {
  'owner': owner,
  'channel': channel,
  'dashboard_url': 'http://127.0.0.1:7071',
  'tick_interval_minutes': 5
}

cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Config salvo em: {cfg_path}')
print('Próximo passo: python orchestrator/scripts/tick.py e python dashboard/server.py')
