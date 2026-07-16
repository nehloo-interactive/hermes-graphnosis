"""Graphnosis memory provider distribution for Hermes Agent.

This package is a *delivery vehicle*. The actual Hermes plugin lives in the
bundled ``graphnosis/`` folder; the ``installer`` module copies it into the
Hermes user plugins directory, where Hermes' directory-based memory-provider
discovery finds it. See the README for why a copy installer is used instead of
a pip entry point.
"""

__version__ = "1.0.0"
