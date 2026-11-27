"""Fixtures for assessment step 201 — the assessment-plan validator.

Puts the step's own scripts/ directory on sys.path (the project's standard resolution: insert the
directory, import the flat module name).
"""
import sys
from pathlib import Path

STEP = (Path(__file__).resolve().parents[3]
        / "process_02_assessment" / "step_201_assessment_plan")
SCRIPTS = STEP / "scripts"
VALIDATOR = SCRIPTS / "validate_assessment_plan.py"

sys.path.insert(0, str(SCRIPTS))
