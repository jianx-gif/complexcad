"""(b) The operation parser / classifier on small inline CadQuery programs.

Operation *detection* in the toolchain is the AST method-call scanner
``parse_ops`` (identical in koor/eval_predictions.py and koor/score_one.py;
the ``ast_*`` columns of _review/parser_audit/audit_sheet.csv). The parameter
*classifier* is ``iso_knowledge.classify_param`` fed by ``params.from_script``
(repository root, imported through the installed package).
"""
import os

import pytest

from koor.eval_predictions import parse_ops, MODELING, COMPLEX
from koor.score_one import parse_ops as parse_ops_score_one

import iso_knowledge as iso
import params

COMPLEX_FIVE = ("chamfer", "fillet", "revolve", "sweep", "loft")

PLAIN_EXTRUDE = """import cadquery as cq
plate_width = 40.0
plate_depth = 25.0
thickness = 4.0
result = cq.Workplane("XY").rect(plate_width, plate_depth).extrude(thickness)
"""

CHAMFER_FILLET = """import cadquery as cq
block = cq.Workplane("XY").box(30, 20, 10)
block = block.edges("|Z").fillet(2.0)
result = block.faces(">Z").edges().chamfer(0.8)
"""

REVOLVE_SWEEP_LOFT = """import cadquery as cq
profile = (cq.Workplane("XZ").moveTo(5, 0).lineTo(10, 0).lineTo(10, 20)
           .lineTo(5, 20).close())
ring = profile.revolve(360, (0, 0, 0), (0, 1, 0))
path = cq.Workplane("XZ").moveTo(0, 0).lineTo(0, 30)
tube = cq.Workplane("XY").circle(2).sweep(path)
funnel = cq.Workplane("XY").rect(10, 10).workplane(offset=12).circle(3).loft()
result = ring.union(tube).union(funnel)
"""

# The one regex/AST disagreement of the parser audit (13_ztc_f09_393): a
# `chamfer_size` identifier and a comment mention, but no .chamfer() call.
IDENTIFIER_ONLY = """import cadquery as cq
chamfer_size = 0.5   # would be a fillet or chamfer if it were applied
fillet_r = 1.0
result = cq.Workplane("XY").box(10, 10, 10)
"""


def test_plain_extrude_has_no_complex_ops():
    ops = parse_ops(PLAIN_EXTRUDE)
    # ast.walk is breadth-first: the outermost call of a chain comes first,
    # so compare as a multiset (exactly one rect + one extrude, nothing else)
    assert sorted(ops) == ["extrude", "rect"]
    assert not any(o in COMPLEX_FIVE for o in ops)
    assert not any(o in COMPLEX for o in ops)


def test_chamfer_and_fillet_detected_once_each():
    ops = parse_ops(CHAMFER_FILLET)
    assert ops.count("fillet") == 1
    assert ops.count("chamfer") == 1
    assert "box" in ops
    assert not any(o in ("revolve", "sweep", "loft") for o in ops)
    # chained helpers (edges/faces) are not modelling operators
    assert "edges" not in ops and "faces" not in ops


def test_revolve_sweep_loft_detected_once_each():
    ops = parse_ops(REVOLVE_SWEEP_LOFT)
    assert ops.count("revolve") == 1
    assert ops.count("sweep") == 1
    assert ops.count("loft") == 1
    assert ops.count("union") == 2
    assert not any(o in ("chamfer", "fillet") for o in ops)
    # every reported op is in the modelling whitelist
    assert all(o in MODELING for o in ops)


def test_identifier_or_comment_is_not_an_operation():
    ops = parse_ops(IDENTIFIER_ONLY)
    assert ops == ["box"]
    assert "chamfer" not in ops and "fillet" not in ops


def test_syntax_error_returns_none():
    assert parse_ops("result = cq.Workplane('XY').box(1, 2,") is None


def test_score_one_parser_agrees_with_eval_predictions_parser():
    for prog in (PLAIN_EXTRUDE, CHAMFER_FILLET, REVOLVE_SWEEP_LOFT, IDENTIFIER_ONLY):
        assert parse_ops_score_one(prog) == parse_ops(prog)


# --- parameter-name classifier (iso_knowledge.classify_param) ---------------
@pytest.mark.parametrize("name, kind", [
    ("chamfer_size", iso.KIND_CHAMFER),
    ("chamfer_distance", iso.KIND_CHAMFER),
    ("fillet_radius", iso.KIND_RADIUS),
    ("corner_radius", iso.KIND_RADIUS),
    ("outer_radius", iso.KIND_DIAMETER),    # radius of a full circle -> diameter
    ("bore_diameter", iso.KIND_DIAMETER),
])
def test_classify_param(name, kind):
    res = iso.classify_param(name)
    assert res is not None, name
    assert res[0] == kind


def test_from_script_extracts_named_params(tmp_path):
    folder = tmp_path / "part"
    folder.mkdir()
    (folder / "cadquery.py").write_text(
        "import cadquery as cq\n"
        "from types import SimpleNamespace as Measures\n"
        "p = Measures(linear_width=45.0, top_fillet=2.5)\n"
        "plate_width = 40.0\n"
        "result = cq.Workplane('XY').box(plate_width, 10, 5).edges('|Z')"
        ".chamfer(0.5)\n", encoding="utf-8")
    got = params.from_script(str(folder))
    assert got["plate_width"] == 40.0
    assert got["linear_width"] == 45.0 and got["top_fillet"] == 2.5
    assert got["chamfer_size"] == 0.5          # synthesised from the literal .chamfer(0.5)
    assert iso.classify_param("chamfer_size")[0] == iso.KIND_CHAMFER
    assert params.from_script(str(tmp_path / "missing")) == {}
