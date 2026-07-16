"""Installer for the Graphnosis memory provider plugin.

Copies the bundled ``graphnosis/`` plugin folder into the Hermes user plugins
directory (``$HERMES_HOME/plugins/graphnosis/``, default
``~/.hermes/plugins/``), where Hermes' directory-based memory-provider
discovery picks it up on the next ``hermes memory setup`` / session start.

Why a copy installer instead of a pip entry point: Hermes (verified against
0.17.0) discovers memory providers ONLY by scanning plugin directories
(``plugins/memory/__init__.py``). Pip entry points are scanned by the general
PluginManager, but a detected memory provider is coerced to ``kind=exclusive``
and handed to memory discovery — which never enumerates entry points — so an
entry-point-only provider is dropped. Directory install is the reliable path.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from importlib import resources
from pathlib import Path
from typing import Optional

PLUGIN_NAME = "graphnosis"


def hermes_plugins_dir() -> Path:
    """Resolve the Hermes user plugins directory.

    Honors ``$HERMES_HOME`` when set, otherwise falls back to ``~/.hermes``.
    """
    home = os.environ.get("HERMES_HOME")
    base = Path(home).expanduser() if home else Path.home() / ".hermes"
    return base / "plugins"


def _bundled_plugin_dir() -> Path:
    """Locate the ``graphnosis/`` folder bundled inside this package."""
    return Path(str(resources.files("hermes_graphnosis").joinpath(PLUGIN_NAME)))


def install(dest: Optional[Path] = None, force: bool = False) -> Path:
    plugins_dir = dest or hermes_plugins_dir()
    target = plugins_dir / PLUGIN_NAME
    src = _bundled_plugin_dir()
    if not (src / "__init__.py").exists():
        raise FileNotFoundError(f"Bundled plugin not found at {src}")
    if target.exists():
        if not force:
            raise FileExistsError(
                f"{target} already exists. Re-run with --force to overwrite."
            )
        shutil.rmtree(target)
    plugins_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        src, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )
    return target


def uninstall(dest: Optional[Path] = None) -> Optional[Path]:
    plugins_dir = dest or hermes_plugins_dir()
    target = plugins_dir / PLUGIN_NAME
    if target.exists():
        shutil.rmtree(target)
        return target
    return None


def status(dest: Optional[Path] = None) -> bool:
    plugins_dir = dest or hermes_plugins_dir()
    target = plugins_dir / PLUGIN_NAME
    return (target / "__init__.py").exists()


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hermes-graphnosis",
        description="Install the Graphnosis memory provider into Hermes Agent.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Target plugins dir (default: $HERMES_HOME/plugins or ~/.hermes/plugins)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_install = sub.add_parser("install", help="Copy the plugin into the Hermes plugins dir")
    p_install.add_argument("--force", action="store_true", help="Overwrite an existing install")
    sub.add_parser("uninstall", help="Remove the installed plugin")
    sub.add_parser("status", help="Show whether the plugin is installed")
    sub.add_parser("path", help="Print the resolved Hermes plugins dir")

    args = parser.parse_args(argv)

    if args.command == "path":
        print(args.dest or hermes_plugins_dir())
        return 0

    if args.command == "status":
        installed = status(args.dest)
        target = (args.dest or hermes_plugins_dir()) / PLUGIN_NAME
        print(f"{'installed' if installed else 'not installed'}: {target}")
        return 0 if installed else 1

    if args.command == "uninstall":
        removed = uninstall(args.dest)
        print(f"Removed {removed}" if removed else "Nothing to remove.")
        return 0

    # install
    try:
        target = install(args.dest, force=getattr(args, "force", False))
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Installed Graphnosis memory provider into {target}")
    print("Next: run `hermes memory setup` and select graphnosis, then start a new session.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
