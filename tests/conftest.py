"""Test bootstrap.

The plugin imports a few Hermes-runtime modules at load time
(`agent.memory_provider`, `tools.registry`). Those only exist inside a Hermes
install. For standalone unit tests we inject minimal stubs so the provider can
be imported and exercised in isolation.
"""

import sys
import types


def _install_hermes_stubs() -> None:
    if "agent.memory_provider" not in sys.modules:
        agent = types.ModuleType("agent")
        mem = types.ModuleType("agent.memory_provider")

        class MemoryProvider:  # minimal stand-in for the real ABC
            pass

        mem.MemoryProvider = MemoryProvider
        agent.memory_provider = mem
        sys.modules["agent"] = agent
        sys.modules["agent.memory_provider"] = mem

    if "tools.registry" not in sys.modules:
        tools = types.ModuleType("tools")
        registry = types.ModuleType("tools.registry")
        registry.tool_error = lambda msg: f"ERROR: {msg}"
        tools.registry = registry
        sys.modules["tools"] = tools
        sys.modules["tools.registry"] = registry


_install_hermes_stubs()
