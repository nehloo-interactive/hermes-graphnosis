"""Tests for the Graphnosis memory provider (standalone)."""

import json

import pytest

from hermes_graphnosis.graphnosis import GraphnosisMemoryProvider


class FakeGraphnosisClient:
    def __init__(self, *args, **kwargs):
        self.calls = []

    def connect(self):
        return None

    def close(self):
        return None

    def call_tool(self, name, arguments=None):
        self.calls.append((name, arguments or {}))
        if name == "recall":
            return "Remembered: user prefers TypeScript."
        if name == "remember":
            return "Saved."
        if name == "stats":
            return "engrams: 3"
        return ""


def test_is_available_when_socket_exists(tmp_path):
    sock = tmp_path / "mcp.sock"
    sock.touch()
    provider = GraphnosisMemoryProvider({"socket_path": str(sock), "prefetch_max_tokens": 500})
    assert provider.is_available() is True


def test_is_available_when_socket_missing():
    provider = GraphnosisMemoryProvider({"socket_path": "/nonexistent/mcp.sock"})
    assert provider.is_available() is False


def test_handle_recall_tool():
    provider = GraphnosisMemoryProvider({"socket_path": "/tmp/mcp.sock", "prefetch_max_tokens": 500})
    provider._client = FakeGraphnosisClient()
    result = json.loads(provider.handle_tool_call("graphnosis_recall", {"query": "typescript preference"}))
    assert "TypeScript" in result["result"]
    assert provider._client.calls[0][0] == "recall"


def test_handle_remember_tool():
    provider = GraphnosisMemoryProvider({"socket_path": "/tmp/mcp.sock", "prefetch_max_tokens": 500})
    provider._client = FakeGraphnosisClient()
    result = json.loads(provider.handle_tool_call("graphnosis_remember", {"text": "User prefers zsh"}))
    assert "Saved" in result["result"]
    assert provider._client.calls[0][0] == "remember"


def test_prefetch_queue():
    provider = GraphnosisMemoryProvider({"socket_path": "/tmp/mcp.sock", "prefetch_max_tokens": 500})
    provider._client = FakeGraphnosisClient()
    provider.queue_prefetch("what are my preferences?")
    if provider._prefetch_thread:
        provider._prefetch_thread.join(timeout=2.0)
    block = provider.prefetch("what are my preferences?")
    assert "Graphnosis Memory" in block or block == ""


def test_installer_roundtrip(tmp_path):
    from hermes_graphnosis import installer

    plugins = tmp_path / "plugins"
    target = installer.install(plugins)
    assert (target / "__init__.py").exists()
    assert installer.status(plugins) is True
    installer.uninstall(plugins)
    assert installer.status(plugins) is False
