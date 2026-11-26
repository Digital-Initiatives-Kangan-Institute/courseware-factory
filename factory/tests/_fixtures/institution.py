"""Minimal test institution pack — lets the institution-agnostic engine be tested without a real one.

A real institution supplies institution.py in its pack (institutions/<name>/); this is a test double.
BODY_STYLE is a style a blank python-docx document carries, so layout renders without a template.
"""
BODY_STYLE = "Body Text"
