"""Temporary DeepSeek-only relay; run in a container separate from the agent."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def read_key() -> str:
    for line in Path("/run/secrets/deepseek.env").read_text(
        encoding="utf-8-sig"
    ).splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            key = line.partition("=")[2].strip().strip('"').strip("'")
            if key:
                return key
    raise RuntimeError("DeepSeek key is absent from the mounted secret file")


def token_count(usage: dict, field: str) -> int | None:
    value = usage.get(field)
    return value if type(value) is int and value >= 0 else None


KEY = ""
UPSTREAM = "https://api.deepseek.com/chat/completions"
MAX_REQUEST_BYTES = 200_000
MAX_RESPONSE_BYTES = 8_000_000
MAX_TOTAL_TOKENS = 500_000
remaining = 25
requests_used = 0
total_tokens = 0


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global remaining, requests_used, total_tokens
        if self.path not in ("/chat/completions", "/v1/chat/completions"):
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error(400)
            return
        if not 0 < length <= MAX_REQUEST_BYTES:
            self.send_error(413 if length > MAX_REQUEST_BYTES else 400)
            return
        body = self.rfile.read(length)
        if remaining <= 0:
            self.send_error(429)
            return
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            self.send_error(400)
            return
        if payload.get("model") != "deepseek-flash":
            self.send_error(400, "Unsupported model")
            return
        if payload.get("stream"):
            self.send_error(400, "Streaming disabled for this probe")
            return
        output_limit = payload.get("max_tokens", payload.get("max_completion_tokens"))
        if type(output_limit) is not int or not 0 < output_limit <= 2048:
            self.send_error(400, "Output token limit exceeded")
            return
        remaining -= 1
        requests_used += 1
        request = Request(
            UPSTREAM,
            data=body,
            headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=60) as response:
                result = response.read(MAX_RESPONSE_BYTES + 1)
                status = response.status
                content_type = response.headers.get("Content-Type", "application/json")
        except HTTPError as error:
            result = error.read(MAX_RESPONSE_BYTES + 1)
            status = error.code
            content_type = "application/json"
        except URLError:
            self.send_error(502, "Model upstream unavailable")
            return
        if len(result) > MAX_RESPONSE_BYTES:
            self.send_error(502, "Model response too large")
            return
        if status == 200:
            try:
                usage = json.loads(result).get("usage", {})
                if not isinstance(usage, dict):
                    raise ValueError("Invalid model usage")
            except (ValueError, AttributeError, UnicodeDecodeError):
                remaining = 0
                self.send_error(502, "Invalid model response")
                return
            request_tokens = token_count(usage, "total_tokens")
            if request_tokens is not None:
                total_tokens += request_tokens
            else:
                remaining = 0
            if total_tokens >= MAX_TOTAL_TOKENS:
                remaining = 0
            print(
                json.dumps(
                    {
                        "requests_used": requests_used,
                        "request_tokens": request_tokens,
                        "prompt_cache_hit_tokens": token_count(usage, "prompt_cache_hit_tokens"),
                        "prompt_cache_miss_tokens": token_count(usage, "prompt_cache_miss_tokens"),
                        "completion_tokens": token_count(usage, "completion_tokens"),
                        "total_tokens": total_tokens,
                        "requests_remaining": remaining,
                    }
                ),
                flush=True,
            )
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(result)))
        self.end_headers()
        self.wfile.write(result)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    KEY = read_key()
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
