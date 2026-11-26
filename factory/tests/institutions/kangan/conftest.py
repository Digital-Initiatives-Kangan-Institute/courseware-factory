"""Put the Kangan institution pack on sys.path for its own tests only.

The pack lives at the repo root (institutions/kangan/), outside factory/, so engine tests never see it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "institutions" / "kangan"))
