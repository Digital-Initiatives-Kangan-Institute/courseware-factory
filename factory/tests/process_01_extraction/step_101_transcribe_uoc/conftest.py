"""Fixtures for extraction step 01 — the UoC transcriber.

Puts the step's own scripts/ directory on sys.path (the project's standard resolution: insert the
directory, import the flat module name). The Word-XML builders come from the shared `docx_fixtures`
module, which the validator's tests will use too.
"""
import sys
from pathlib import Path

STEP = (Path(__file__).resolve().parents[3]
        / "process_01_extraction" / "step_101_transcribe_uoc")
SCRIPTS = STEP / "scripts"
TRANSCRIBER = SCRIPTS / "transcribe_uoc.py"
VALIDATOR = SCRIPTS / "validate_uoc.py"

sys.path.insert(0, str(SCRIPTS))
