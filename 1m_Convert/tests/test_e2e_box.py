"""(c) Tiny end-to-end check: execute a 5-line CadQuery box program through the
toolchain's own exec helpers and count its faces (= 6), plus the quantisation
transform round trip on the same program."""
import pytest

cq = pytest.importorskip("cadquery")

from koor.koor_transform import scale_code, collect_lengths


def test_box_has_six_faces_via_score_one_exec_shape(box_program):
    from koor.score_one import exec_shape            # exec helper used by the scorer
    shape = exec_shape(box_program)
    assert shape is not None
    assert len(shape.Faces()) == 6
    assert len(shape.Edges()) == 12 and len(shape.Vertices()) == 8
    bb = shape.BoundingBox()
    assert (round(bb.xlen, 6), round(bb.ylen, 6), round(bb.zlen, 6)) == (20.0, 10.0, 5.0)
    assert shape.Volume() == pytest.approx(20 * 10 * 5)


def test_box_via_build_koor_geometry_exec_to_shape(box_program, tmp_path):
    # importing this module also imports `match` from the repository root, i.e.
    # it proves the root modules are importable through the installed package
    from koor import build_koor_geometry as bkg
    r = bkg.exec_to_shape(box_program)
    assert len(r.val().Faces()) == 6
    # the minimal-metadata writer lists the modelling calls of the program
    bkg._write_min_metadata(str(tmp_path), "test-uuid", box_program)
    import json
    meta = json.load(open(tmp_path / "metadata.json", encoding="utf-8"))
    names = [o["op_name"] for o in meta["cadquery_ops_json"]]
    assert "box" in names and meta["cadquery_ops_count"] == len(names)
    assert not any(n in ("chamfer", "fillet", "revolve", "sweep", "loft") for n in names)


def test_quantised_program_executes_to_scaled_box(box_program):
    from koor.score_one import exec_shape
    new_src, stats = scale_code(box_program, scale=100)
    assert stats["n_scaled"] == 3 and stats["n_clamped"] == 0
    assert "2000" in new_src and "1000" in new_src and "500" in new_src
    assert sorted(collect_lengths(box_program)) == [5.0, 10.0, 20.0]
    bb = exec_shape(new_src).BoundingBox()
    assert (round(bb.xlen), round(bb.ylen), round(bb.zlen)) == (2000, 1000, 500)
