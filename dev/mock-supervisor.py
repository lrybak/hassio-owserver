"""Minimal mock of the Home Assistant Supervisor API for local addon development."""

import http.server
import json
import os

OPTIONS_PATH = os.environ.get("OPTIONS_PATH", "/data/options.json")

ADDON_INFO = {
    "result": "ok",
    "data": {
        "log_level": "info",
        "name": "owserver (1-wire)",
        "slug": "owserver",
        "version": "dev",
        "description": "owserver dev",
        "hostname": "localhost",
        "boot": "auto",
        "options": {},
        "ports": {"4304/tcp": 4304, "8099/tcp": 8099},
    },
}


def _load_options():
    """Load options.json and return as supervisor config response."""
    try:
        with open(OPTIONS_PATH) as f:
            return {"result": "ok", "data": json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"result": "ok", "data": {}}


class Handler(http.server.BaseHTTPRequestHandler):
    def _respond(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/addons/self/options/config":
            self._respond(_load_options())
        else:
            self._respond(ADDON_INFO)

    def do_POST(self):
        if self.headers.get("Content-Length"):
            self.rfile.read(int(self.headers["Content-Length"]))
        self._respond(ADDON_INFO)

    def log_message(self, fmt, *args):
        print(f"[supervisor mock] {self.path} {args[1]}")


if __name__ == "__main__":
    server = http.server.HTTPServer(("", 80), Handler)
    print("[supervisor mock] listening on :80")
    server.serve_forever()
