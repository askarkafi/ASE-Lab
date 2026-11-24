"""Temporary DeepSeek-only relay; run in a container separate from the agent."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import RemoteDisconnected
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
analysis_budget = False
MAX_ANALYSIS_TOOL_CHARS = 2400
TRUNCATED_TOOL_OUTPUT = "\n[Tool output truncated by ASE-Lab]"


def truncate_tool_output(content):
    if isinstance(content, str):
        if len(content) > MAX_ANALYSIS_TOOL_CHARS:
            return content[:MAX_ANALYSIS_TOOL_CHARS] + TRUNCATED_TOOL_OUTPUT
        return content
    if not isinstance(content, list):
        return content

    # OpenHands sends tool observations as a list of typed content parts.
    parts = []
    remaining_chars = MAX_ANALYSIS_TOOL_CHARS
    truncated = False
    for part in content:
        if part.get("type") != "text":
            parts.append(part)
            continue
        text = part["text"]
        if len(text) <= remaining_chars:
            parts.append(part)
            remaining_chars -= len(text)
        elif not truncated:
            parts.append({**part, "text": text[:remaining_chars] + TRUNCATED_TOOL_OUTPUT})
            remaining_chars = 0
            truncated = True
    return parts


def analysis_payload(payload: dict, final_turn: bool) -> bytes:
    """Bound tool context and reserve the last request for a report."""
    for message in payload["messages"]:
        if message.get("role") == "tool":
            message["content"] = truncate_tool_output(message.get("content"))
    if final_turn:
        finish = [tool for tool in payload.get("tools", [])
                  if tool.get("function", {}).get("name") == "finish"]
        if len(finish) != 1:
            raise ValueError("Missing finish tool")
        payload["tools"] = finish
        payload["tool_choice"] = {"type": "function", "function": {"name": "finish"}}
        payload["thinking"] = {"type": "disabled"}
        payload["messages"].append({"role": "user", "content":
            "Search budget ended. Call finish now with the requested JSON using only evidence already gathered. "
            "Report supported findings and remaining uncertainty. If none are supported, return an inconclusive answer."})
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def local_budget_error(handler: BaseHTTPRequestHandler) -> None:
    """Reject a spent local allowance without suggesting an upstream rate limit."""
    body = json.dumps({"error": {"message": "ASE-Lab local relay budget exhausted",
                                  "type": "invalid_request_error",
                                  "code": "ase_lab_budget_exhausted"}}).encode()
    handler.send_response(400)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


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
            local_budget_error(self)
            return
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            self.send_error(400)
            return
        if not isinstance(payload, dict) or payload.get("model") != "deepseek-flash":
            self.send_error(400, "Unsupported model")
            return
        if payload.get("stream"):
            self.send_error(400, "Streaming disabled for this probe")
            return
        output_limit = payload.get("max_tokens", payload.get("max_completion_tokens"))
        if type(output_limit) is not int or not 0 < output_limit <= 2048:
            self.send_error(400, "Output token limit exceeded")
            return
        final_turn = analysis_budget and remaining == 1
        if analysis_budget:
            try:
                body = analysis_payload(payload, final_turn)
            except (KeyError, TypeError, AttributeError, ValueError):
                self.send_error(400, "Invalid analysis request")
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
        except (URLError, RemoteDisconnected, TimeoutError, ConnectionError):
            print(json.dumps({"event": "upstream_transport_error",
                              "requests_used": requests_used,
                              "total_tokens": total_tokens,
                              "usage_unknown_for_request": True}), flush=True)
            self.send_error(502, "Model upstream unavailable")
            return
        if len(result) > MAX_RESPONSE_BYTES:
            self.send_error(502, "Model response too large")
            return
        if status == 200:
            try:
                completion = json.loads(result)
                usage = completion.get("usage", {})
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
                        **({"final_turn": final_turn} if analysis_budget else {}),
                    }
                ),
                flush=True,
            )
            if final_turn:
                try:
                    choices = completion["choices"]
                    calls = choices[0]["message"]["tool_calls"]
                    valid_finish = (len(choices) == 1 and len(calls) == 1
                                    and calls[0]["function"]["name"] == "finish")
                except (KeyError, IndexError, TypeError):
                    valid_finish = False
                if not valid_finish:
                    self.send_error(422, "Analysis final turn requires one finish call")
                    return
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
