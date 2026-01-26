#!/usr/bin/env python3
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def get_version() -> str:
    return os.getenv("APP_VERSION") or os.getenv("VERSION") or "dev"

def get_git_sha() -> str:
    return os.getenv("GIT_SHA") or "unknown"

def get_app_name() -> str:
    return os.getenv("APP_NAME") or "versioned-app"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/healthz":
            body = b"ok\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path != "/":
            body = b"not found\n"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        msg = f"{get_app_name()} v{get_version()} ({get_git_sha()})\n".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def log_message(self, fmt: str, *args) -> None:
        # Keep logs minimal and deterministic
        return


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer((host, port), Handler)
    print(f"listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
