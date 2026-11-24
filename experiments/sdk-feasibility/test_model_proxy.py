"""Focused offline checks for the temporary relay's usage limit."""

import importlib.util
import json
import threading
import unittest
from contextlib import closing
from http.client import HTTPConnection
from http.client import RemoteDisconnected
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
        proxy.analysis_budget = False
        server = proxy.HTTPServer(("127.0.0.1", 0), proxy.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, timeout=3)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def post(self, server, **fields):
        body = json.dumps(
            {"model": "deepseek-flash", "max_tokens": 8, "stream": False, **fields}
        )
        with closing(HTTPConnection("127.0.0.1", server.server_port, timeout=3)) as client:
            client.request("POST", "/chat/completions", body)
            response = client.getresponse()
            return response.status, response.read()

    def test_usage_limit_stops_next_request(self):
        server = self.start_server()
        with patch.object(proxy, "urlopen", return_value=FakeResponse()) as upstream:
            self.assertEqual(self.post(server)[0], 200)
            self.assertEqual(proxy.total_tokens, 500_000)
            status, body = self.post(server)
            self.assertEqual(status, 400)
            self.assertEqual(json.loads(body)["error"]["code"], "ase_lab_budget_exhausted")
            self.assertEqual(upstream.call_count, 1)

    def test_request_allowance_stops_without_upstream_call(self):
        server = self.start_server()
        proxy.remaining = 0
        with patch.object(proxy, "urlopen") as upstream:
            status, body = self.post(server)
            self.assertEqual(status, 400)
            self.assertEqual(json.loads(body)["error"]["code"], "ase_lab_budget_exhausted")
            upstream.assert_not_called()

    def test_malformed_response_closes_relay(self):
        server = self.start_server()
        with patch.object(proxy, "urlopen", return_value=FakeResponse(b"invalid")) as upstream:
            self.assertEqual(self.post(server)[0], 502)
            self.assertEqual(self.post(server)[0], 400)
            self.assertEqual(upstream.call_count, 1)

    def test_upstream_disconnect_returns_502_and_records_unknown_usage(self):
        server = self.start_server()
        with patch.object(proxy, "urlopen", side_effect=RemoteDisconnected("closed")):
            with patch("builtins.print") as logged:
                status, _ = self.post(server)
        self.assertEqual(status, 502)
        self.assertEqual(proxy.requests_used, 1)
        record = json.loads(logged.call_args.args[0])
        self.assertEqual(record["event"], "upstream_transport_error")
        self.assertTrue(record["usage_unknown_for_request"])

    def test_analysis_reserves_last_request_for_finish_and_trims_tool_context(self):
        server = self.start_server()
        proxy.analysis_budget = True
        proxy.remaining = 2
        tools = [{"type": "function", "function": {"name": name}} for name in ("terminal", "finish")]
        evidence = "first relevant line\n" + "x" * 3000
        messages = [{"role": "tool", "content": evidence}]
        def response(name):
            return FakeResponse(json.dumps({
                "choices": [{"message": {"tool_calls": [{"function": {"name": name}}]}}],
                "usage": {"total_tokens": 42},
            }).encode())
        with patch.object(proxy, "urlopen", side_effect=[response("terminal"), response("terminal")]) as upstream:
            self.assertEqual(self.post(server, messages=messages, tools=tools)[0], 200)
            self.assertEqual(self.post(server, messages=messages, tools=tools)[0], 422)
            self.assertEqual(self.post(server, messages=messages, tools=tools)[0], 400)
        first, last = [json.loads(call.args[0].data) for call in upstream.call_args_list]
        self.assertEqual(first["tools"], tools)
        self.assertEqual(last["tools"], tools[1:])
        self.assertEqual(last["tool_choice"]["function"]["name"], "finish")
        self.assertEqual(last["thinking"], {"type": "disabled"})
        self.assertEqual(first["messages"][0]["content"],
                         evidence[:proxy.MAX_ANALYSIS_TOOL_CHARS] + "\n[Tool output truncated by ASE-Lab]")


if __name__ == "__main__":
    unittest.main()
