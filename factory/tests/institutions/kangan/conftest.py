"""Make the Kangan institution pack the active one — for each Kangan test only.

The pack lives at the repo root (institutions/kangan/), outside factory/. Its `institution` module has
the same name as every other pack's and as the suite's neutral test double, so it cannot simply be put
on sys.path for the session: whichever got there first would win for every test, and the suite's result
would depend on collection order. Instead each test here gets the pack on the path and the pack's
`institution` in place, engine modules that read it rebuilt against it, and all of that undone after.
"""
import importlib
import sys
from pathlib import Path

import pytest

PACK = Path(__file__).resolve().parents[4] / "institutions" / "kangan"

# Engine modules that bind institution values at import, so must be rebuilt when the pack changes.
_BOUND_TO_INSTITUTION = ["instrument_layout"]
# Modules that live in the pack.
_PACK_MODULES = ["institution", "kangan_deck", "instrument_template"]


@pytest.fixture(autouse=True)
def kangan_pack():
    saved = {name: sys.modules.get(name) for name in _PACK_MODULES}
    for name in _PACK_MODULES:
        sys.modules.pop(name, None)
    sys.path.insert(0, str(PACK))
    for name in _BOUND_TO_INSTITUTION:
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    try:
        yield PACK
    finally:
        sys.path.remove(str(PACK))
        for name in _PACK_MODULES:
            sys.modules.pop(name, None)
            if saved[name] is not None:
                sys.modules[name] = saved[name]
        for name in _BOUND_TO_INSTITUTION:
            if name in sys.modules:
                importlib.reload(sys.modules[name])
