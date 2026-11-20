"""Focused offline checks for the temporary relay's usage limit."""

import importlib.util
import json
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("model_proxy.py")
spec = importlib.util.spec_from_file_location("model_proxy", MODULE_PATH)
assert spec and spec.loader
proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proxy)


class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/json"}

    def __init__(self, body=None):
        self.body = body or json.dumps(
            {"choices": [], "usage": {"total_tokens": 500_000}}
        ).encode()

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit):
        return self.body


class RelayTests(unittest.TestCase):
    def start_server(self):
        proxy.KEY = "fake-only"
        proxy.remaining = 25
        proxy.requests_used = 0
        proxy.total_tokens = 0
        server = proxy.HTTPServer(("127.0.0.1", 0), proxy.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, timeout=3)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def post(self, server):
        body = json.dumps(
            {"model": "deepseek-flash", "max_tokens": 8, "stream": False}
        )
        with closing(HTTPConnection("127.0.0.1", server.server_port, timeout=3)) as client:
            client.request("POST", "/chat/completions", body)
            response = client.getresponse()
            response.read()
            return response.status

    def test_usage_limit_stops_next_request(self):
        server = self.start_server()
        with patch.object(proxy, "urlopen", return_value=FakeResponse()) as upstream:
            self.assertEqual(self.post(server), 200)
            self.assertEqual(proxy.total_tokens, 500_000)
            self.assertEqual(self.post(server), 429)
            self.assertEqual(upstream.call_count, 1)

    def test_malformed_response_closes_relay(self):
        server = self.start_server()
        with patch.object(proxy, "urlopen", return_value=FakeResponse(b"invalid")) as upstream:
            self.assertEqual(self.post(server), 502)
            self.assertEqual(self.post(server), 429)
            self.assertEqual(upstream.call_count, 1)


if __name__ == "__main__":
    unittest.main()
