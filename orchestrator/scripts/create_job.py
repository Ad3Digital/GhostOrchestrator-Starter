import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'jobs' / 'queue.json'


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_queue():
    if not QUEUE.exists():
        return {'version': 1, 'jobs': []}
    return json.loads(QUEUE.read_text(encoding='utf-8'))


def save_queue(data):
    QUEUE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--goal', required=True)
    p.add_argument('--owner_agent', default='main')
    p.add_argument('--risk', default='low', choices=['low', 'medium', 'high'])
    p.add_argument('--then', action='append', default=[])
    args = p.parse_args()

    q = load_queue()
    ts = now_iso()
    job = {
        'job_id': str(uuid.uuid4()),
        'title': args.title,
        'goal': args.goal,
        'owner_agent': args.owner_agent,
        'risk_level': args.risk,
        'needs_human_approval': args.risk == 'high',
        'status': 'backlog',
        'created_at': ts,
        'updated_at': ts,
        'retry_count': 0,
        'max_retries': 2,
        'then': args.then,
        'then_created': False,
        'notes': []
    }
    q['jobs'].append(job)
    save_queue(q)
    print('CREATED', job['job_id'])
