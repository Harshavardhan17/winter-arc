"""Tiny in-memory stand-in for the Firebase Realtime Database REST API (GET/PUT/DELETE + SSE) for local testing."""
import json, threading, time, sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

DATA = {}
LOCK = threading.Lock()
VERSION = [0]
OFFLINE = [False]

def parts(path):
    p = path.split("?")[0]
    assert p.endswith(".json")
    return [x for x in p[:-5].split("/") if x]

def get(ps):
    node = DATA
    for k in ps:
        if not isinstance(node, dict) or k not in node:
            return None
        node = node[k]
    return node

def put(ps, value):
    node = DATA
    trail = []
    for k in ps[:-1]:
        trail.append((node, k))
        node = node.setdefault(k, {})
    if value is None:
        node.pop(ps[-1], None)
        for parent, k in reversed(trail):
            if parent.get(k) == {}:
                parent.pop(k)
    else:
        node[ps[-1]] = value
    VERSION[0] += 1

class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    def reply(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code); self.cors()
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(200); self.cors(); self.end_headers()
    def do_GET(self):
        if self.path.startswith("/__offline"):
            OFFLINE[0] = self.path.endswith("on"); return self.reply(OFFLINE[0])
        if OFFLINE[0]: return self.reply({"error": "offline"}, 503)
        ps = parts(self.path)
        if "text/event-stream" in self.headers.get("Accept", ""):
            self.send_response(200); self.cors()
            self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            seen = -1
            try:
                while True:
                    if VERSION[0] != seen:
                        seen = VERSION[0]
                        with LOCK: d = get(ps)
                        self.wfile.write(f"event: put\ndata: {json.dumps({'path': '/', 'data': d})}\n\n".encode()); self.wfile.flush()
                    time.sleep(0.3)
            except Exception:
                return
        with LOCK: self.reply(get(ps))
    def do_PUT(self):
        if OFFLINE[0]: return self.reply({"error": "offline"}, 503)
        n = int(self.headers.get("Content-Length", 0))
        v = json.loads(self.rfile.read(n) or b"null")
        with LOCK: put(parts(self.path), v)
        self.reply(v)
    def do_DELETE(self):
        if OFFLINE[0]: return self.reply({"error": "offline"}, 503)
        with LOCK: put(parts(self.path), None)
        self.reply(None)
    def log_message(self, *a): pass

ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8788), H).serve_forever()
