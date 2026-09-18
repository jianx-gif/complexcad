"""Shared fixtures. The tests need no dataset: they use small inline CadQuery
programs, temporary directories and the CLI help paths only."""
import os
import subprocess
import sys

import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TESTS_DIR)          # .../1m_Convert
ROOT_DIR = os.path.dirname(PROJECT_DIR)           # .../data (drawing core modules)

BOX_PROGRAM = """import cadquery as cq
width = 20.0
depth = 10.0
height = 5.0
result = cq.Workplane("XY").box(width, depth, height)
"""


@pytest.fixture(scope="session")
def box_program():
    """A 5-line CadQuery program building one 20 x 10 x 5 box (6 faces)."""
    return BOX_PROGRAM


@pytest.fixture(scope="session")
def project_dir():
    return PROJECT_DIR


@pytest.fixture(scope="session")
def root_dir():
    return ROOT_DIR


@pytest.fixture(scope="session")
def run_koor():
    """Run ``python -m koor <args>`` in a fresh interpreter and return the
    CompletedProcess (utf-8 text). Works before and after ``pip install -e``."""
    def _run(*args, input=None, env=None, timeout=120):
        e = dict(os.environ)
        e["PYTHONIOENCODING"] = "utf-8"
        e["PYTHONPATH"] = os.pathsep.join(
            [PROJECT_DIR, ROOT_DIR] + [p for p in [e.get("PYTHONPATH")] if p])
        if env:
            e.update(env)
        return subprocess.run([sys.executable, "-X", "utf8", "-m", "koor", *args],
                              input=input, capture_output=True, text=True,
                              encoding="utf-8", env=e, timeout=timeout)
    return _run
