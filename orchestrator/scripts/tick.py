import json
from datetime import datetime, timezone
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'jobs' / 'queue.json'
HISTORY = ROOT / 'jobs' / 'history.jsonl'


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_queue():
    return json.loads(QUEUE.read_text(encoding='utf-8'))


def save_queue(data):
    QUEUE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def log(event):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def enqueue_followups(q, job):
    if job.get('then_created') or not job.get('then'):
        return
    for step in job['then']:
        ts = now_iso()
        child = {
            'job_id': str(uuid.uuid4()),
            'parent_job_id': job['job_id'],
            'title': f"Follow-up: {step[:60]}",
            'goal': step,
            'owner_agent': job.get('owner_agent', 'main'),
            'risk_level': job.get('risk_level', 'low'),
            'needs_human_approval': job.get('risk_level', 'low') == 'high',
            'status': 'backlog',
            'created_at': ts,
            'updated_at': ts,
            'retry_count': 0,
            'max_retries': job.get('max_retries', 2),
            'then': [],
            'then_created': True,
            'notes': [f'Auto-criado de {job["job_id"]}']
        }
        q['jobs'].append(child)
        log({'ts': ts, 'event': 'followup_created', 'job_id': child['job_id'], 'parent_job_id': job['job_id']})
    job['then_created'] = True


def process_job(job):
    ts = now_iso()
    if job['status'] == 'backlog':
        job['status'] = 'in_progress'
        job['updated_at'] = ts
        log({'ts': ts, 'event': 'job_started', 'job_id': job['job_id']})
        return

    if job['status'] == 'in_progress':
        if job.get('needs_human_approval'):
            job['status'] = 'review'
            job['updated_at'] = ts
            log({'ts': ts, 'event': 'job_review_required', 'job_id': job['job_id']})
            return

        # sucesso padrão (MVP)
        job['status'] = 'done'
        job['updated_at'] = ts
        log({'ts': ts, 'event': 'job_done', 'job_id': job['job_id']})


if __name__ == '__main__':
    q = load_queue()

    # Processa 1 job por ciclo para previsibilidade
    for job in q.get('jobs', []):
        if job.get('status') in ('backlog', 'in_progress'):
            process_job(job)
            break

    # Gera continuidade automática em jobs concluídos
    for job in q.get('jobs', []):
        if job.get('status') == 'done':
            enqueue_followups(q, job)

    save_queue(q)
    print('TICK_OK')
