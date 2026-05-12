"""
common.py — Episode 3 shared imports.
Re-exports Episode 1 + Episode 2 assets.
"""
import sys, os
import importlib.util

_EP3_DIR = os.path.dirname(os.path.abspath(__file__))
_EP1_DIR = os.path.join(_EP3_DIR, "..", "Episode1")
_EP2_DIR = os.path.join(_EP3_DIR, "..", "Episode2")


def _load_module(name, filepath):
    """Load a Python file as a named module without affecting sys.path."""
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# --- Load Episode 1 common (colors + helpers) ---
_ep1 = _load_module("ep1_common", os.path.join(_EP1_DIR, "common.py"))

# Re-export everything from ep1 into this namespace
from ep1_common import *  # noqa: F401, F403

# --- Load TEAL_EP2 from Episode 2 common ---
_ep2 = _load_module("ep2_common", os.path.join(_EP2_DIR, "common.py"))
TEAL_EP2 = _ep2.TEAL_EP2  # "#14B8A6"

_ASSETS = os.path.join(_EP3_DIR, "assets")
