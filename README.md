# Graphnosis memory provider for Hermes Agent

Local, encrypted, on-device memory for [Hermes Agent](https://github.com/NousResearch/hermes-agent) via the [Graphnosis](https://graphnosis.com) desktop app — engrams, semantic recall, auto-prefetch, and (optionally) skills. No API key, nothing leaves your machine.

This is a **standalone plugin**, published separately per the Hermes
[memory-provider policy](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md) (`plugins/memory/` is closed to new in-tree backends).

## Prerequisites

1. [Install Graphnosis](https://graphnosis.com/download) and unlock your cortex (the app must be running).
2. Confirm the MCP socket exists: `~/.graphnosis/mcp.sock`.
3. A working Hermes Agent install.

## Install

### Option A — pip + installer (recommended)

```bash
pip install hermes-graphnosis
hermes-graphnosis install          # copies the plugin into ~/.hermes/plugins/graphnosis/
```

`hermes-graphnosis` also supports `status`, `uninstall`, `path`, and
`install --force`. It honors `$HERMES_HOME` (defaults to `~/.hermes`).

> **Why an installer, not a pip entry point?** Hermes (as of 0.17.0) discovers
> memory providers **only by scanning plugin directories** — see
> [`plugins/memory/__init__.py`](https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/__init__.py).
> A pip *entry point* for a memory provider is detected by the general
> PluginManager but coerced to `kind=exclusive` and handed to memory discovery,
> which never enumerates entry points — so it is silently dropped. The installer
> copies the plugin into the directory Hermes actually scans.

### Option B — drop-in directory (no pip)

```bash
git clone https://github.com/nehloo-interactive/hermes-graphnosis
cp -R hermes-graphnosis/src/hermes_graphnosis/graphnosis ~/.hermes/plugins/graphnosis
```

## Activate

```bash
hermes memory setup            # select "graphnosis"
hermes graphnosis status       # verify socket + cortex connectivity
```

Start a new Hermes session after setup.

## Recommended: also install the MCP catalog entry

The memory provider gives you `graphnosis_recall`, `graphnosis_remember`, and
`graphnosis_stats`. For the full tool surface — `edit`, `forget`,
`cross_search`, skills, consent — add the Graphnosis MCP server. The manifest
is bundled at `src/hermes_graphnosis/data/mcp-manifest.yaml`; register it in
`~/.hermes/config.yaml`:

```yaml
mcp_servers:
  graphnosis:
    command: npx
    args: ["-y", "@graphnosis/mcp-relay", "${HOME}/.graphnosis/mcp.sock"]
    enabled: true
```

These appear as `mcp_graphnosis_*` tools in Hermes sessions.

Optional recall-hygiene skill:

```bash
hermes skills install https://graphnosis.com/skills/graphnosis/SKILL.md
```

## Configuration

Settings live in `$HERMES_HOME/graphnosis.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `socket_path` | `~/.graphnosis/mcp.sock` | Graphnosis MCP socket path |
| `default_engram` | `""` | Default engram for `graphnosis_remember` |
| `prefetch_max_tokens` | `1500` | Prefetch token budget per turn |

## CLI

```bash
hermes graphnosis status
hermes graphnosis test-recall "project priorities"
```

Available only when `memory.provider: graphnosis` is active.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Socket not found | Open Graphnosis and unlock the cortex; check `~/.graphnosis/mcp.sock` |
| Recall returns "locked" | Unlock the cortex in the app |
| Provider inactive | Set `memory.provider: graphnosis` in `~/.hermes/config.yaml` |
| `hermes graphnosis` unknown | Re-run `hermes-graphnosis install`; start a fresh session |

Full docs: [graphnosis.com/getting-started/connect-ai](https://graphnosis.com/getting-started/connect-ai)

## License

Apache-2.0. See [LICENSE](LICENSE).
