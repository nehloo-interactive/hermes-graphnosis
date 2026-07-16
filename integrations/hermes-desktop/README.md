# Graphnosis integration for Hermes Desktop

PR-ready patches for [fathah/hermes-desktop](https://github.com/fathah/hermes-desktop).

These are **UI-only** patches — copy, a download link, a one-click MCP-server
install, and an onboarding card. All memory-provider logic lives in the
standalone [`hermes-graphnosis`](https://github.com/nehloo-interactive/hermes-graphnosis)
plugin, which Hermes Desktop picks up automatically because it runs Hermes
Agent underneath. There is **no dependency on any in-tree hermes-agent change.**

## Apply

```bash
DESKTOP=/path/to/hermes-desktop

# Memory providers screen: description + download link
patch -d "$DESKTOP" -p1 < patches/memory-graphnosis-i18n.patch
patch -d "$DESKTOP" -p1 < patches/MemoryProviders-graphnosis.patch

# Register graphnosis in the known-providers map (so the description key resolves)
patch -d "$DESKTOP" -p1 < patches/memory-provider-known-map.patch

# Capabilities → MCP Servers: one-click install card + Graphnosis download
patch -d "$DESKTOP" -p1 < patches/tools-graphnosis-mcp-card.patch

# Welcome / Get Connected onboarding card
patch -d "$DESKTOP" -p1 < patches/welcome-graphnosis-onboarding.patch

# Shared styles for welcome + tools promo cards
patch -d "$DESKTOP" -p1 < patches/graphnosis-ui-styles.patch
```

The "Install Graphnosis MCP" button registers the MCP server directly via
`addMcpServer` (writes `npx -y @graphnosis/mcp-relay ${HOME}/.graphnosis/mcp.sock`
to the user's Hermes config) — it does **not** call a hermes-agent catalog
preset, so it works on a stock Hermes Agent.

## Depends on

- The [`hermes-graphnosis`](https://github.com/nehloo-interactive/hermes-graphnosis)
  standalone plugin (the memory provider itself; the UI here just installs the
  MCP server and links the download).

## Notes

- The Graphnosis memory provider appears on the Memory screen once the user
  installs the standalone plugin (`hermes-graphnosis install`); these patches
  add its label, description, and provider URL.
- Patches are authored against an earlier `fathah/hermes-desktop` commit and
  may need rebasing against current `main` before submitting the PR.
- A previous `graphnosis-mcp-discover.patch` (Discover → bundled MCP catalog
  entry) was **removed**: it read the Graphnosis manifest from
  `$HERMES_HOME/hermes-agent/optional-mcps/graphnosis/` — an artifact that only
  existed in the now-closed in-tree PR. The Tools-screen install card replaces
  it.
