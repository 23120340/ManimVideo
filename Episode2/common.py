"""
common.py — Episode 2 shared imports.
Re-exports Episode 1 assets via importlib (no duplication) + Ep2 additions.
"""
import sys, os
import importlib.util

_EP2_DIR = os.path.dirname(os.path.abspath(__file__))
_EP1_DIR = os.path.join(_EP2_DIR, "..", "Episode1")


def _load_module(name, filepath):
    """Load a Python file as a named module without affecting sys.path."""
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load Episode 1 common (colors + helpers) and re-export everything.
_ep1 = _load_module("ep1_common", os.path.join(_EP1_DIR, "common.py"))
from ep1_common import *  # noqa: F401, F403

# Ep2-specific additions
TEAL_EP2 = "#14B8A6"
_ASSETS = os.path.join(_EP2_DIR, "assets")
