import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'jobs' / 'queue.json'
HISTORY = ROOT / 'jobs' / 'history.jsonl'
INDEX = Path(__file__).resolve().parent / 'index.html'

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        b = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == '/':
            self._send(200, INDEX.read_text(encoding='utf-8'), 'text/html; charset=utf-8')
            return
        if u.path == '/api/queue':
            data = json.loads(QUEUE.read_text(encoding='utf-8')) if QUEUE.exists() else {'version':1,'jobs':[]}
            self._send(200, json.dumps(data, ensure_ascii=False))
            return
        if u.path == '/api/history':
            q = parse_qs(u.query)
            limit = int((q.get('limit') or ['20'])[0])
            events = []
            if HISTORY.exists():
                for line in HISTORY.read_text(encoding='utf-8', errors='ignore').splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        pass
            events = events[-limit:]
            self._send(200, json.dumps({'events': events}, ensure_ascii=False))
            return
        self._send(404, json.dumps({'error':'not found'}))

if __name__ == '__main__':
    port = 7071
    print(f'Dashboard em http://127.0.0.1:{port}')
    ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
