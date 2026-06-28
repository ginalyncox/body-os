"""Local sync HTTP server for companion app ↔ robot data exchange."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING

from .config import RobotConfig
from .data.store import DataStore
from .data.sync_transform import robot_bundle_to_companion

if TYPE_CHECKING:
    pass


class SyncHandler(BaseHTTPRequestHandler):
    config: RobotConfig
    store: DataStore

    def log_message(self, format: str, *args) -> None:
        print(f"   [sync] {self.address_string()} {format % args}")

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:
        if self.path in ("/api/sync", "/api/health"):
            export = self.store.export_all()
            bundle = robot_bundle_to_companion(export)
            bundle["tier"] = self.config.tier
            bundle["robot_name"] = self.config.name
            self._json_response(200, bundle)
            return
        self._json_response(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/sync":
            self._json_response(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            bundle = json.loads(raw)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid json"})
            return

        counts = self.store.merge_companion_bundle(bundle)
        if bundle.get("tier") in ("green", "yellow", "red", "black"):
            self.config.tier = bundle["tier"]
            self.config.save_tier(bundle["tier"])

        self._json_response(200, {"ok": True, "merged": counts})


def make_handler(config: RobotConfig, store: DataStore) -> type[SyncHandler]:
    class Handler(SyncHandler):
        pass

    Handler.config = config
    Handler.store = store
    return Handler


def run_sync_server(config: RobotConfig, store: DataStore, host: str, port: int) -> HTTPServer:
    handler = make_handler(config, store)
    server = HTTPServer((host, port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"   [sync] server at http://{host}:{port}/api/sync")
    return server
