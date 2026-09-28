import os, json
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
import projlib
import drawing
import params
import match

OUT = "output"
# hidden/visible line-length ratio above which a view is replaced by a full
# SECTION A-A (dense internal detail; dimensioning hidden lines is non-standard).
# Calibrated on the first-1000 scan (section_scan.csv): the baseline for ANY 3D
# part is ~1-3 (its own back silhouette is hidden), median 2.25, p90 = 4.4.
# 4.0 selects the ~13% most internally-complex parts -- the cavity/tray/housing
# class -- and leaves plain plates, discs and brackets in normal three views.
SECTION_RATIO = 4.0

def load_step(path):
    reader = STEPControl_Reader()
    if reader.ReadFile(path) != IFSelect_RetDone:
        raise RuntimeError("STEP read failed")
    reader.TransferRoots()
    return reader.OneShape()


def _sweep_degenerate(folder):
    """True if the script HAS a .sweep() but it produced a zero-volume body
    (so no swept feature exists in the part). projlib._reexec returns None
    on exactly that condition; distinguish it from 'no sweep at all'."""
    try:
        if not projlib._SWEEP_ARG.search(
                open(os.path.join(folder, "cadquery.py"), encoding="utf-8").read()):
            return False                       # not a swept part at all
        res, _ = projlib._reexec(folder)
        return res is None                     # has sweep, but it degenerated
    except Exception:
        return False


def _is_phantom_sweep_param(name):
    """A build param meaningful ONLY for the (now non-existent) swept body:
    pipe/tube wall thickness and inner/bore diameter. The OUTER profile diameter
    is kept (it usually also sizes a real stub/cylinder that survives), and real
    body params (flange_thickness, plate_thickness) are kept -- only wall/bore of
    a pipe/tube/duct are dropped."""
    n = name.lower()
    if "wall" in n:
        return True                                   # pipe_wall_thickness
    if ("inner_dia" in n or "inner_diameter" in n or "bore" in n or
            "id" == n.rsplit("_", 1)[-1]):
        return True                                   # inner / bore diameter
    return False

def process(uuid, fmts=("png", "svg", "dxf"), deflection=0.1):
    folder = os.path.join(OUT, uuid)
    step = os.path.join(folder, "model.step")
    # SWEEP PARTS: re-exec the script and pose the (solid + path) TOGETHER, then
    # use that SAME posed solid for the views. This guarantees the path centreline
    # shares the views' pose and overlays exactly. Posing the STEP solid and the
    # re-exec solid separately gives slightly different poses (OBB axis ambiguity)
    # and the path never lines up -- so for swept parts we draw from the re-exec
    # solid, not model.step. Non-swept parts keep using model.step.
    sweep = None
    shape = None
    try:
        posed_solid, path_edges = projlib.posed_solid_and_path(folder)
        if posed_solid is not None and path_edges:
            shape = posed_solid
            # clip the path centreline to the actual posed SOLID (inside-or-near
            # its surface) so phantom path beyond the fabricated part -- an elbow
            # arc whose far half has no pipe, an over-long helix wire -- is not
            # drawn floating outside the model silhouette.
            sweep = projlib.describe_edges(path_edges, clip_solid=posed_solid)
    except Exception:
        shape = None
        sweep = None
    if shape is None:                       # non-swept (or extraction failed)
        shape = load_step(step)
        shape = projlib.normalize_pose(shape)   # re-pose: principal axes -> XYZ
    views = {}
    for name, p in projlib.VIEWS.items():
        views[name] = projlib.project(shape, p["paper_x"], p["paper_y"], deflection=deflection)
    # SECTION VIEW: when one ortho view's hidden/visible ratio is high, its
    # internal detail can't be dimensioned to standard (ISO discourages dims on
    # hidden lines) -- replace that view with a full section A-A through the
    # origin plane and hatch the cut faces. The ISO pictorial stays intact.
    section = None
    try:
        ratios = {v: projlib.hidden_ratio(views[v])
                  for v in ("front", "top", "left")}
        vbest = max(ratios, key=ratios.get)
        if ratios[vbest] >= SECTION_RATIO:
            # Candidate cutting planes: the centre plane plus the top internal-
            # feature stations (hole axes / hidden-detail density, read from the
            # adjacent view). The PURPOSE of the section is to expose internal
            # structure for DIMENSIONING, so each candidate is test-cut and
            # scored by the VISIBLE line length of the resulting view -- voids
            # and bores sliced open become visible (dimensionable) edges, so
            # more visible length = more internal structure revealed. The
            # winning candidate's projection is reused directly.
            cands = [0.0]
            for s in projlib.section_plane_stations(shape, vbest, views, k=3):
                if all(abs(s - c) > 1e-6 for c in cands):
                    cands.append(s)
            p = projlib.VIEWS[vbest]
            best = None              # (score, off, view_dict, faces)
            for off in cands:
                try:
                    half, faces = projlib.section_cut(shape, vbest, offset=off)
                    if not faces:
                        continue
                    sv = projlib.project(half, p["paper_x"], p["paper_y"],
                                         deflection=deflection)
                except Exception:
                    continue
                vis = sum(
                    ((pl[i+1][0]-pl[i][0])**2 + (pl[i+1][1]-pl[i][1])**2) ** 0.5
                    for pl in sv.get("visible", []) for i in range(len(pl)-1))
                if best is None or vis > best[0]:
                    best = (vis, off, sv, faces)
            if best is not None:
                _vis, off, sv, faces = best
                views[vbest] = sv
                section = {"view": vbest, "faces": faces, "offset": off}
    except Exception:
        section = None
    out_prefix = os.path.join(folder, "drawing")
    # read model complexity (cadquery_ops_count) to size the dim buffer
    ops_count = None
    meta_path = os.path.join(folder, "metadata.json")
    if os.path.isfile(meta_path):
        try:
            ops_count = json.load(open(meta_path, encoding="utf-8")).get("cadquery_ops_count")
        except Exception:
            ops_count = None
    # extract build parameters and match them to view geometry for ISO dimensioning
    matched, overall = [], []
    try:
        p = params.extract(folder)
        # If a swept feature DEGENERATED (zero-volume sweep, e.g. a profile plane
        # parallel to the path tangent) the swept body does not exist in the part.
        # Its profile-only parameters -- wall thickness, inner/bore diameter --
        # then have NO matching geometry, so the matcher would pin them onto an
        # unrelated edge of coincidentally-equal length (a 5mm wall stamped on a
        # flange). Drop those phantom params so they are never mis-dimensioned.
        if _sweep_degenerate(folder):
            p = {k: v for k, v in p.items()
                 if not _is_phantom_sweep_param(k)}
        circ = projlib.circles_for_views(shape)
        fillets = projlib.fillet_radii(shape)
        chamfers = projlib.chamfer_sizes(shape)
        bevels = projlib.chamfer_bevels(shape)
        rects = projlib.rect_features(shape)
        vm = {k: views[k] for k in ("front", "top", "left")}
        matched, _ = match.match_params(p, vm, circ, fillets_by_view=fillets,
                                        chamfers_by_view=chamfers,
                                        bevels_by_view=bevels,
                                        rects_by_view=rects)
        overall = match.overall_dims(vm, p)
        # INTERNAL sizes from OPPOSING WALL pairs: a through-slot/channel has no
        # pocket floor for rect_features and often no single intact edge for the
        # matcher, but its two bounding walls always exist in the solid. This
        # relocates value-matching params onto the real feature and adds the
        # small internal gaps nothing else dimensioned.
        try:
            walls = projlib.wall_gap_dims(shape)
            matched = match.wall_dims(matched, walls, vm, overall=overall)
        except Exception:
            pass
        # LOCATION dimensions (ISO: size AND position): locate each hole-group's
        # reference instance and each pocket/boss centre from the datum edges.
        # Sizes/pitches alone leave the reader unable to PLACE the features.
        for v in ("top", "front", "left"):
            try:
                matched = list(matched) + match.location_dims(
                    v, vm[v], circ.get(v), rects.get(v), matched)
            except Exception:
                pass
        # SWEPT-ANGLE (张角) of arc / sector / revolved parts: detect circular-arc
        # edges that read as a true arc in a view and annotate their angular
        # extent (ISO 129-1 angular dimension, unit deg, symbol °). Only fires
        # when a real non-full arc exists, so prismatic parts get no phantom angle.
        try:
            arc_angles = projlib.arc_angles_for_views(shape)
            matched = match.arc_angle_dims(matched, arc_angles, views_model=vm)
        except Exception:
            pass
    except Exception:
        matched, overall = [], []
    # The POINT of a section is dimensioning internals: read wall thicknesses,
    # cavity widths/heights straight off the cut faces and add the linear dims
    # the parameter matching missed (value-deduped against existing dims).
    if section:
        try:
            matched = list(matched) + match.section_dims(
                section["view"], section["faces"], matched, overall=overall)
        except Exception:
            pass
    # `sweep` (path description) was computed above from the SAME posed solid as
    # the views, so it overlays exactly. Nothing to recompute here.
    # Mass for the title block (grams) = volume(mm^3) * steel density 7.85e-6 kg/mm^3.
    part_mass = None
    try:
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp
        pr = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, pr)
        part_mass = pr.Mass() * 7.85e-6 * 1000.0     # mm^3 -> g
    except Exception:
        part_mass = None
    # ISO 128 centre lines: the axis of every hole, boss and shaft (projlib.hole_axes)
    # becomes a centre cross where it is seen axis-on and an axis line where it is
    # seen from the side. Model-view coords; drawing.render scales and extends them.
    centre_marks = []
    try:
        centre_marks = projlib.centre_marks_for_views(shape)
    except Exception:
        centre_marks = []
    paper, scale, results = drawing.render(
        views, uuid, out_prefix, fmts=fmts, ops_count=ops_count,
        matched=matched, overall=overall, sweep=sweep, section=section,
        mass=part_mass, title=uuid, centre_marks=centre_marks)
    return paper, scale, results

# `process(uuid)` is the single entry point: it loads output/<uuid>/model.step,
# applies the unified sweep + standard ISO dimensioning rules, and writes
# drawing.{png,svg,dxf} into that folder. Batch generation over output/ is driven
# by regen_all.py (e.g. `python regen_all.py 0 1000` for the first 1000 parts).
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        paper, scale, results = process(sys.argv[1])
        print(f"{sys.argv[1]} -> {paper} 1:{drawing._scale_str(scale)} {list(results)}")
    else:
        print("usage: python make_drawings.py <uuid>   "
              "(batch: python regen_all.py [offset] [count])")
