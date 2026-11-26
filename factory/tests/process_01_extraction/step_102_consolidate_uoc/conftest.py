"""Fixtures for extraction step 02 — consolidating a cluster's units of competency.

Puts the step's own scripts/ directory on sys.path (the project's standard resolution: insert the
directory, import the flat module name).
"""
import sys
from pathlib import Path

STEP = (Path(__file__).resolve().parents[3]
        / "process_01_extraction" / "step_102_consolidate_uoc")
SCRIPTS = STEP / "scripts"
INVENTORY = SCRIPTS / "inventory_uoc.py"
ITEMS_VALIDATOR = SCRIPTS / "validate_consolidated_items.py"

sys.path.insert(0, str(SCRIPTS))
