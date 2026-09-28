"""Augment each part in output/<uuid>/ with the modalities the thesis requires
but the pipeline did not yet emit:

  1. point_cloud.npy  -- N surface points + per-point normals (point cloud modality)
  2. point_cloud.ply  -- same, human-viewable
  3. model.brep       -- BREP export (task wants STEP/BREP/STL)
  4. metadata.json    -- add geometry stats: edge/vertex counts, bbox dims
  5. description.json  + description.txt -- TEXT modality:
        structured ops + NL operation-sequence + feature/dimension text +
        design-intent free text.

Self-contained, resilient (per-part errors logged & skipped), progress logged.
Usage:  python augment_data.py [offset] [count]   (default: all of output/)
"""
import ast
import json
import os
import sys
import time
import traceback

import numpy as np
import trimesh

from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepTools import BRepTools
from OCP.TopExp import TopExp_Explorer, TopExp
from OCP.TopAbs import TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

import params as params_mod
import iso_knowledge as iso
import text_params

OUT = "output"
N_POINTS = 8192


# --------------------------------------------------------------------------- #
# geometry helpers
# --------------------------------------------------------------------------- #
def load_step(path):
    r = STEPControl_Reader()
    if r.ReadFile(path) != IFSelect_RetDone:
        raise RuntimeError("STEP read failed")
    r.TransferRoots()
    return r.OneShape()


def _count_unique(shape, typ):
    """Count UNIQUE sub-shapes of a type (each edge/vertex is shared by several
    faces; a raw explorer over-counts, so map to dedup)."""
    m = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, typ, m)
    return m.Extent()


def geometry_stats(shape):
    nf = _count_unique(shape, TopAbs_FACE)
    ne = _count_unique(shape, TopAbs_EDGE)
    nv = _count_unique(shape, TopAbs_VERTEX)
    b = Bnd_Box()
    BRepBndLib.Add_s(shape, b)
    xmin, ymin, zmin, xmax, ymax, zmax = b.Get()
    return {
        "num_faces": nf,
        "num_edges": ne,
        "num_vertices": nv,
        "bbox_min": [round(xmin, 4), round(ymin, 4), round(zmin, 4)],
        "bbox_max": [round(xmax, 4), round(ymax, 4), round(zmax, 4)],
        "bbox_dims": [round(xmax - xmin, 4), round(ymax - ymin, 4),
                      round(zmax - zmin, 4)],
    }


def sample_point_cloud(stl_path, n=N_POINTS, seed=None):
    """N surface points + per-point normals from the STL. Returns (pts, normals)
    as float32 arrays, or (None, None) on failure."""
    mesh = trimesh.load(stl_path, process=False)
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = mesh.dump(concatenate=True)
    # seed: per-model seed (first 8 hex digits of the UUID) since 2026-09-17 -> reproducible point set;
    # the released clouds were sampled unseeded (distribution-consistent, not point-identical).
    pts, fidx = trimesh.sample.sample_surface(mesh, n, seed=seed)
    normals = mesh.face_normals[fidx]
    return pts.astype("float32"), normals.astype("float32")


def write_ply(path, pts, normals):
    with open(path, "w", encoding="ascii") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write("element vertex %d\n" % len(pts))
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property float nx\nproperty float ny\nproperty float nz\n")
        f.write("end_header\n")
        for (x, y, z), (nx, ny, nz) in zip(pts, normals):
            f.write("%.5f %.5f %.5f %.5f %.5f %.5f\n" % (x, y, z, nx, ny, nz))


# --------------------------------------------------------------------------- #
# TEXT modality
# --------------------------------------------------------------------------- #
# Real modelling ops (drop Python control-flow noise that the AST scraper logs).
_REAL_OPS = {
    "extrude", "cut", "hole", "cboreHole", "cskHole", "fillet", "chamfer",
    "revolve", "sweep", "loft", "union", "intersect", "shell", "box",
    "circle", "rect", "polygon", "polyline", "cutBlind", "cutThruAll",
    "twistExtrude", "mirror",
}
_OP_PHRASE = {
    "extrude": "extrude a profile into a solid",
    "cut": "subtract material with a boolean cut",
    "hole": "drill a through hole",
    "cboreHole": "drill a counterbored hole",
    "cskHole": "drill a countersunk hole",
    "fillet": "round an edge with a fillet",
    "chamfer": "bevel an edge with a chamfer",
    "revolve": "revolve a profile about an axis",
    "sweep": "sweep a profile along a path",
    "loft": "loft between multiple sections",
    "union": "merge solids with a boolean union",
    "intersect": "keep the boolean intersection of solids",
    "shell": "hollow the solid into a shell",
    "box": "create a box primitive",
    "cutBlind": "cut a blind pocket",
    "cutThruAll": "cut a through slot",
    "twistExtrude": "extrude a profile with a twist",
    "mirror": "mirror the geometry",
}


# 2D sketch primitives: they define a profile but are not modelling steps. The
# human review of 2026-09-17 rejected 194/200 step lists mainly because these
# were listed as steps (188 of the 194). They are excluded from the sequence.
_SKETCH_PRIMITIVES = {"circle", "rect", "polygon", "polyline"}


def _real_ops(ops_json):
    """Modelling steps in CONSTRUCTION order.

    The upstream ops log lists the outermost call of every chain first (a
    breadth-first walk of the AST), so 'fillet' at line 67 could precede
    'cutBlind' at line 30. Steps are therefore sorted by their source position
    (lineno, col_offset), which is the order in which a straight-line CadQuery
    script executes them, and 2D sketch primitives are dropped.
    Calls of one chained expression (``.box().edges().chamfer()``) share the
    position of the expression's start, so within a chain the depth of the call
    in the chain (the number of dotted members of the logged ``function`` path)
    orders the steps: the inner call executes first."""
    rows = []
    for i, op in enumerate(ops_json or []):
        name = op.get("op_name")
        if name in _REAL_OPS and name not in _SKETCH_PRIMITIVES:
            depth = str(op.get("function") or "").count(".")
            rows.append((op.get("lineno") or 0, op.get("col_offset") or 0, depth, i, name))
    rows.sort()
    return [r[4] for r in rows]


def steps_from_source(folder, ops_json=None):
    """Modelling steps in EXECUTION order, read from the program itself.

    The program (cadquery.py) is the ground truth of the text modality, so its
    abstract syntax tree is parsed directly: every method call whose name is a
    3D modelling operation is taken at the position where the call CLOSES
    (end_lineno, end_col_offset). In a chained expression the inner call closes
    first, and a call nested in an argument -- result.union(cq.Workplane()
    .rect(a, b).extrude(h)) -- closes before the call that consumes it, so
    the end positions give the order in which a straight-line script executes
    the operations. A loop body is listed once, as written. 2D sketch
    primitives are not steps. Falls back to the upstream operation log
    (_real_ops) when the source cannot be parsed."""
    path = os.path.join(folder, "cadquery.py")
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(src)
    except Exception:
        return _real_ops(ops_json)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            name = node.func.attr
            if name in _REAL_OPS and name not in _SKETCH_PRIMITIVES:
                calls.append((node.end_lineno or 0, node.end_col_offset or 0, name))
    calls.sort()
    return [c[2] for c in calls] or _real_ops(ops_json)


def _classified_params(prm):
    """Split params into dimensioned categories using the ISO classifier, so the
    feature/dimension text groups them the way an engineer reads a drawing."""
    groups = {}
    for name, val in prm.items():
        c = text_params.classify_param(name)
        kind = c[0] if c else "other"
        groups.setdefault(kind, []).append((name, val))
    return groups


def build_description(folder, ops_json, stats):
    """Return (structured_dict, free_text). Covers the four text sub-types the
    task lists: operation-sequence NL, feature/dimension text, design intent,
    plus a structured form."""
    prm = text_params.extract(folder)
    ops = steps_from_source(folder, ops_json)
    # operation-sequence natural language
    op_counts = {}
    for o in ops:
        op_counts[o] = op_counts.get(o, 0) + 1
    seq_sentences = []
    for i, o in enumerate(ops, 1):
        seq_sentences.append("%d. %s" % (i, _OP_PHRASE.get(o, o)))
    seq_nl = ("The part is built in %d modelling steps: " % len(ops)
              + "; ".join(_OP_PHRASE.get(o, o) for o in ops) + ".") if ops else \
             "The part is built from sketch-extrude operations."
    # feature / dimension text
    groups = _classified_params(prm)
    feat_bits = []
    label = {"diameter": "hole/cylinder diameters", "radius": "fillet/round radii",
             "chamfer": "chamfer sizes", "linear_h": "lengths", "linear_v": "heights",
             "depth": "depths", "angle": "angles", "position": "feature spacings"}
    for kind, items in groups.items():
        if kind == "other":
            continue
        vals = ", ".join("%s=%s" % (n, _fmt(v)) for n, v in items)
        feat_bits.append("%s: %s" % (label.get(kind, kind), vals))
    feature_text = ("Key dimensions -- " + "; ".join(feat_bits) + ".") if feat_bits \
        else "Dimensions are defined parametrically in the build script."
    bb = stats["bbox_dims"]
    geom_text = ("The part spans %.1f x %.1f x %.1f mm and has %d faces, "
                 "%d edges, %d vertices." %
                 (bb[0], bb[1], bb[2], stats["num_faces"],
                  stats["num_edges"], stats["num_vertices"]))
    # design intent (heuristic from which ops/features are present)
    intent = _design_intent(op_counts, groups)
    # free text = the human-readable paragraph
    free_text = " ".join([seq_nl, feature_text, geom_text, intent])
    structured = {
        "operation_sequence": ops,
        "operation_counts": op_counts,
        "operation_sequence_steps": seq_sentences,
        "parameters": {k: v for k, v in prm.items()},
        "parameter_groups": {k: dict(v) for k, v in groups.items()},
        "geometry": {"bbox_dims_mm": bb, "num_faces": stats["num_faces"],
                     "num_edges": stats["num_edges"],
                     "num_vertices": stats["num_vertices"]},
        "design_intent": intent,
    }
    return structured, free_text


def _fmt(v):
    try:
        f = float(v)
        return ("%g" % f)
    except (TypeError, ValueError):
        return str(v)


def _design_intent(op_counts, groups):
    bits = []
    if op_counts.get("hole", 0) + op_counts.get("cboreHole", 0) \
            + op_counts.get("cskHole", 0) >= 2:
        bits.append("a mounting component with multiple fastening holes")
    if op_counts.get("revolve"):
        bits.append("a body of revolution (shaft/disc-like)")
    if op_counts.get("sweep"):
        bits.append("a swept profile following a path (pipe/rail-like)")
    if op_counts.get("loft"):
        bits.append("a lofted transition between cross-sections")
    if op_counts.get("fillet") or op_counts.get("chamfer"):
        bits.append("edge treatments (fillets/chamfers) for stress relief or "
                    "assembly clearance")
    if op_counts.get("shell"):
        bits.append("a thin-walled / hollow design")
    if not bits:
        bits.append("a prismatic bracket/plate built by sketch-extrude")
    return "Design intent: the model represents " + "; ".join(bits) + "."


# --------------------------------------------------------------------------- #
# per-part driver
# --------------------------------------------------------------------------- #
def augment(uuid):
    folder = os.path.join(OUT, uuid)
    step = os.path.join(folder, "model.step")
    stl = os.path.join(folder, "model.stl")
    meta_path = os.path.join(folder, "metadata.json")
    shape = load_step(step)

    # 2 + 4: BREP export and geometry stats
    BRepTools.Write_s(shape, os.path.join(folder, "model.brep"))
    stats = geometry_stats(shape)

    # 1: point cloud
    pts, normals = sample_point_cloud(stl, seed=int(uuid[:8], 16))
    np.save(os.path.join(folder, "point_cloud.npy"),
            np.concatenate([pts, normals], axis=1))      # (N,6): xyz + normal
    write_ply(os.path.join(folder, "point_cloud.ply"), pts, normals)

    # load metadata, merge stats
    meta = {}
    if os.path.isfile(meta_path):
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except Exception:
            meta = {}
    meta.setdefault("uuid", uuid)
    meta["geometry_stats"] = stats
    meta["num_points"] = int(len(pts))

    # 5: text modality
    structured, free_text = build_description(folder, meta.get("cadquery_ops_json"),
                                              stats)
    json.dump(structured, open(os.path.join(folder, "description.json"), "w",
                               encoding="utf-8"), indent=2, ensure_ascii=False)
    open(os.path.join(folder, "description.txt"), "w",
         encoding="utf-8").write(free_text + "\n")
    meta["has_point_cloud"] = True
    meta["has_brep"] = True
    meta["has_text_description"] = True
    json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=2,
              ensure_ascii=False)


def main():
    us = sorted(d for d in os.listdir(OUT)
                if os.path.isdir(os.path.join(OUT, d))
                and os.path.isfile(os.path.join(OUT, d, "model.step")))
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    us = us[start:]
    if len(sys.argv) > 2:
        us = us[:int(sys.argv[2])]
    total = len(us)
    print("AUGMENT START total=%d (offset=%d)" % (total, start), flush=True)
    ok = fail = 0
    t0 = time.time()
    for i, u in enumerate(us):
        try:
            augment(u)
            ok += 1
        except Exception as e:
            fail += 1
            print("FAIL %s: %s" % (u, e), flush=True)
            traceback.print_exc()
        if (i + 1) % 50 == 0 or (i + 1) == total:
            dt = time.time() - t0
            rate = (i + 1) / dt if dt else 0
            eta = (total - (i + 1)) / rate if rate else 0
            print("PROGRESS %d/%d ok=%d fail=%d %.2f/s ETA=%.1fmin"
                  % (i + 1, total, ok, fail, rate, eta / 60), flush=True)
    print("AUGMENT DONE ok=%d fail=%d elapsed=%.1fmin"
          % (ok, fail, (time.time() - t0) / 60), flush=True)


if __name__ == "__main__":
    main()
