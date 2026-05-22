"""
Local HTTP server for the Discord cache viewer gallery.
Run: python server.py
Then open http://localhost:8765 in your browser.
"""

import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

from extractor import extract_images, find_discord_cache

OUTPUT_DIR = Path(__file__).parent / "extracted"
UI_DIR = Path(__file__).parent / "ui"
PORT = 8765


def build_image_manifest() -> list[dict]:
    images = []
    for f in sorted(OUTPUT_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            stat = f.stat()
            images.append({
                "name": f.name,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "ext": f.suffix.lstrip(".").upper(),
            })
    return images


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress request logs

    def _send(self, code: int, ctype: str, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_file(UI_DIR / "index.html", "text/html")

        elif path == "/style.css":
            self._serve_file(UI_DIR / "style.css", "text/css")

        elif path == "/app.js":
            self._serve_file(UI_DIR / "app.js", "application/javascript")

        elif path == "/api/images":
            if not OUTPUT_DIR.exists():
                data = json.dumps([]).encode()
            else:
                data = json.dumps(build_image_manifest()).encode()
            self._send(200, "application/json", data)

        elif path == "/api/extract":
            cache_dir = find_discord_cache()
            if cache_dir is None:
                self._send(404, "application/json", b'{"error":"Discord cache not found"}')
                return
            results = extract_images(cache_dir, OUTPUT_DIR)
            payload = json.dumps({"extracted": len(results)}).encode()
            self._send(200, "application/json", payload)

        elif path.startswith("/images/"):
            filename = unquote(path[len("/images/"):])
            self._serve_file(OUTPUT_DIR / filename, self._mime(filename))

        else:
            self._send(404, "text/plain", b"Not found")

    def _serve_file(self, filepath: Path, ctype: str):
        try:
            self._send(200, ctype, filepath.read_bytes())
        except (FileNotFoundError, OSError):
            self._send(404, "text/plain", b"Not found")

    @staticmethod
    def _mime(name: str) -> str:
        ext = Path(name).suffix.lower()
        return {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".webp": "image/webp",
        }.get(ext, "application/octet-stream")


def main():
    server = HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"Discord Cache Viewer running at {url}")
    print("Press Ctrl+C to stop.\n")

    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
