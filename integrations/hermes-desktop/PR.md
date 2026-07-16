# Pull request: Graphnosis UI for Hermes Desktop

Open against https://github.com/fathah/hermes-desktop

## Title

feat(memory): Graphnosis provider surfaces, MCP install, and onboarding

## Summary

- English i18n description for the `graphnosis` memory provider
- Website link to graphnosis.com/download on the Memory Providers screen
- **Capabilities → MCP Servers:** one-click Graphnosis MCP install (registers
  the stdio server directly via `addMcpServer`) + app download link
- **Welcome:** Get Connected onboarding card linking to graphnosis.com/download

UI only — no dependency on any in-tree hermes-agent change. The memory provider
itself ships as the standalone
[`hermes-graphnosis`](https://github.com/nehloo-interactive/hermes-graphnosis)
plugin, which Hermes Desktop discovers automatically (it runs Hermes Agent
underneath).

Apply patches from `patches/` or copy changes from this bundle.

## Depends on

- The standalone [`hermes-graphnosis`](https://github.com/nehloo-interactive/hermes-graphnosis)
  plugin (memory provider). The UI patches themselves have no build-time
  dependency on it.

## Test plan

- [ ] Memory screen shows the Graphnosis provider (label + description + URL)
      once the `hermes-graphnosis` plugin is installed
- [ ] External links open graphnosis.com/download
- [ ] Capabilities → MCP shows the Graphnosis promo when the `graphnosis`
      server is not installed; Install registers it and it appears in the list
- [ ] Installing does not require any hermes-agent catalog preset (stock Agent)
- [ ] Welcome screen shows the Graphnosis onboarding card with download link
