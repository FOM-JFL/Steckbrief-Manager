"""
Steckbrief-Manager – Statischer HTTP-Server
Dient die index.html und zugehörige Assets auf dem konfigurierten PORT aus.
"""

import os
import sys
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 6111))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    """Serve files from the project directory with CORS headers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        # Flush immediately so PM2 captures output
        sys.stdout.write("[Steckbrief-Manager] %s\n" % (format % args))
        sys.stdout.flush()


def main():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Steckbrief-Manager läuft auf http://0.0.0.0:{PORT}")
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")
        server.server_close()


if __name__ == "__main__":
    main()
