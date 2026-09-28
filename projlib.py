"""
ISO 5456-2 multi-view projection library.
Projects an OCC shape (loaded from STEP) into 2D edge sets for:
  front / top / left views (first-angle) + isometric.
Uses OCC HLR (Hidden Line Removal) to split visible vs hidden edges.
Returns 2D polyline segments in mm, in a consistent paper coordinate frame.
"""
import math
import os
import re
import cadquery as cq
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax1, gp_Ax2, gp_Ax3, gp_Pnt, gp_Dir, gp_Trsf, gp_Vec, gp_Pln
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_VERTEX
from OCP.BRep import BRep_Tool, BRep_Builder
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone,
                         GeomAbs_Torus, GeomAbs_Circle, GeomAbs_Line,
                         GeomAbs_BSplineCurve)
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.Bnd import Bnd_Box, Bnd_OBB
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform


def _largest_planar_normal(shape, with_dominance=False):
    """Return the unit normal (gp_Dir) of the largest-area planar face, or None.

    With `with_dominance`, also return how much that face DOMINATES the rest:
    (normal, ratio) where ratio = largest_area / (largest area among planar faces
    whose normal is NOT parallel to it). A high ratio means one flat face clearly
    governs the part's orientation (a base plate); ~1 means several comparable
    faces at different angles (a wedge/prism) where 'the largest' is ambiguous."""
    best_area, best_n = 0.0, None
    faces = []                       # (area, gp_Dir) for all planar faces
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Plane:
            props = GProp_GProps()
            BRepGProp.SurfaceProperties_s(face, props)
            area = props.Mass()
            n = surf.Plane().Axis().Direction()
            faces.append((area, n))
            if area > best_area:
                best_area, best_n = area, n
        exp.Next()
    if not with_dominance:
        return best_n
    if best_n is None:
        return None, 1.0
    # largest area among faces NOT parallel to the winner (a different orientation)
    other = 0.0
    for area, n in faces:
        if abs(n.X() * best_n.X() + n.Y() * best_n.Y()
               + n.Z() * best_n.Z()) < 0.98:
            other = max(other, area)
    ratio = best_area / other if other > 1e-9 else float("inf")
    return best_n, ratio


REV_AREA_FRAC = 0.35   # min fraction of total area on the dominant revolution
                       # axis for a part to count as a body of revolution
                       # (keeps plates-with-holes from being misclassified)


def _revolution_axis(shape):
    """Return the dominant revolution-axis direction (tuple) IF cylinder/cone/
    torus faces sharing one axis carry at least REV_AREA_FRAC of the total
    surface area; else None. This distinguishes a real revolved body from a
    prismatic part that merely has a few round holes."""
    buckets = []        # [dir(tuple), area_on_axis]
    total_area = 0.0
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        surf = BRepAdaptor_Surface(face)
        st = surf.GetType()
        pr = GProp_GProps(); BRepGProp.SurfaceProperties_s(face, pr)
        a = pr.Mass(); total_area += a
        ax = None
        if st == GeomAbs_Cylinder:
            ax = surf.Cylinder().Axis().Direction()
        elif st == GeomAbs_Cone:
            ax = surf.Cone().Axis().Direction()
        elif st == GeomAbs_Torus:
            ax = surf.Torus().Axis().Direction()
        if ax is not None:
            d = (ax.X(), ax.Y(), ax.Z())
            placed = False
            for bucket in buckets:
                bd = bucket[0]
                if abs(bd[0]*d[0] + bd[1]*d[1] + bd[2]*d[2]) > 0.98:   # collinear
                    bucket[1] += a; placed = True; break
            if not placed:
                buckets.append([d, a])
        exp.Next()
    if not buckets or total_area < 1e-9:
        return None
    buckets.sort(key=lambda b: b[1], reverse=True)
    if buckets[0][1] / total_area < REV_AREA_FRAC:
        return None        # round faces too minor -> treat as prismatic
    return buckets[0][0]


def is_revolved(shape):
    """True if the shape has a dominant revolution axis that is currently aligned
    to a world axis (used by the regression check)."""
    d = _revolution_axis(shape)
    if d is None:
        return False
    m = max(abs(d[0]), abs(d[1]), abs(d[2]))
    return m >= math.cos(math.radians(3.0))   # within 3 deg of a world axis


def normalize_pose(shape):
    """Re-pose a shape so its principal directions align to the world axes.
    Hybrid strategy (revolved vs prismatic), because no single rule fits both:
      - body of revolution -> align its revolution axis to a world axis (OBB is
        unreliable here: near-equal axes make the axis order ambiguous);
      - otherwise -> minimum-volume OBB (robust for plates/wedges/skew parts).
    Then a common Z-up (mass) and in-plane refine."""
    rev = _revolution_axis(shape)
    if rev is not None:
        posed = _pose_revolved(shape, rev)
    else:
        posed = _pose_prismatic(shape)

    # In-plane refine: snap the dominant top-view edge direction to the axes so
    # plate/feature edges read parallel to the frame (not a few-degree diamond).
    posed = _align_inplane_z(posed)

    # Z-sign: heavier (mass-concentrated) end faces DOWN, so TOP looks down onto
    # the lighter/open end.
    if not _z_points_up(posed):
        t2 = gp_Trsf()
        t2.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi)
        posed = BRepBuilderAPI_Transform(posed, t2, True).Shape()
    return posed


def _pose_revolved(shape, axis):
    """Align a body of revolution: put its revolution axis along Z if the part
    is disc-like (axis = shortest extent) or along X if it is shaft-like
    (axis = longest extent), then centre at the origin."""
    # First bring the revolution axis onto +Z (centroid to origin).
    props = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, props)
    com = props.CentreOfMass()
    t0 = gp_Trsf(); t0.SetTranslation(gp_Vec(-com.X(), -com.Y(), -com.Z()))
    centred = BRepBuilderAPI_Transform(shape, t0, True).Shape()
    onz = _align_dir_to_z(centred, axis)
    # Measure extent along the axis (now Z) vs across it.
    ax, ay, az, bx, by, bz = _bbox(onz)
    along = bz - az
    across = max(bx - ax, by - ay)
    if along > 1.5 * across:
        # shaft-like: lay the axis horizontal (Z -> X), long side along width
        t = gp_Trsf()
        t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), -math.pi / 2.0)
        return BRepBuilderAPI_Transform(onz, t, True).Shape()
    return onz   # disc-like: axis stays vertical (largest circular face up)


def _pose_prismatic(shape):
    """Minimum-volume OBB alignment for non-revolved parts: longest edge -> X,
    shortest -> Z (largest face horizontal), middle -> Y; then snap a near-
    horizontal top face exactly flat."""
    obb = Bnd_OBB()
    BRepBndLib.AddOBB_s(shape, obb, True, True, True)
    c = obb.Center()
    axes = [(obb.XHSize(), obb.XDirection()),
            (obb.YHSize(), obb.YDirection()),
            (obb.ZHSize(), obb.ZDirection())]
    axes.sort(key=lambda a: a[0], reverse=True)
    long_d, short_d = axes[0][1], axes[2][1]
    src = gp_Ax3(gp_Pnt(c.X(), c.Y(), c.Z()),
                 gp_Dir(short_d.X(), short_d.Y(), short_d.Z()),
                 gp_Dir(long_d.X(), long_d.Y(), long_d.Z()))
    dst = gp_Ax3(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1), gp_Dir(1, 0, 0))
    t1 = gp_Trsf(); t1.SetTransformation(dst, src)
    posed = BRepBuilderAPI_Transform(shape, t1, True).Shape()
    # Snap the part's dominant flat face to horizontal. The min-volume OBB aligns
    # the BOUNDING BOX, but for curved/swept parts (an arc-swept bracket, a bent
    # bar) the box axes can sit 20-30 deg off the part's actual base face, leaving
    # the drawing visibly tilted. So if the largest planar face is the part's
    # clear PRIMARY face (its area dominates the next-largest plane) we trust it
    # and snap it flat even when it is well off-axis; otherwise (several similar
    # faces -> a wedge/prism where snapping the "largest" is ambiguous) we keep
    # the tighter near-flat threshold to avoid laying a genuine slope flat.
    n, dom = _largest_planar_normal(posed, with_dominance=True)
    if n is not None:
        tilt = abs(n.Z())
        primary = dom >= 1.6                       # >=60% bigger than next plane
        thresh = 40.0 if primary else 15.0
        if tilt >= math.cos(math.radians(thresh)):
            posed = _align_dir_to_z(posed, (n.X(), n.Y(), n.Z()))
    return posed


def _bbox(shape):
    b = Bnd_Box(); BRepBndLib.Add_s(shape, b)
    return b.Get()


def _hole_pattern_angle(shape):
    """If the part has a regular ring of holes (a bolt pattern) but no dominant
    rectangular frame to align to, return the small Z-rotation (radians) that
    lays that pattern on the X/Y axes (holes at 0/90/180/270), else None.

    Round/disc parts have no straight main frame, so _align_inplane_z's edge
    histogram locks onto whatever incidental slot/tessellation angle dominates
    and leaves the bolt holes skewed (an X-pattern instead of +-pattern). The
    holes themselves are the natural in-plane reference: when >=3 of them share
    one angle (mod 90), snap that angle to the axes."""
    circ = circles_for_views(shape)
    pts = [(cx, cy) for (r, cx, cy, is_full, is_hole, _cov) in circ.get("top", [])
           if is_hole and math.hypot(cx, cy) > 1.0]
    if len(pts) < 3:
        return None
    angs = [math.degrees(math.atan2(cy, cx)) % 90.0 for cx, cy in pts]
    # fold near the 0/90 wrap so e.g. 89 and 1 average correctly, then check the
    # spread: a genuine regular pattern has all spokes at the SAME angle (mod 90).
    base = angs[0]
    folded = []
    for a in angs:
        d = a - base
        if d > 45.0:
            d -= 90.0
        elif d < -45.0:
            d += 90.0
        folded.append(d)
    spread = max(folded) - min(folded)
    if spread > 6.0:                       # not a coherent single-angle pattern
        return None
    dom = base + sum(folded) / len(folded)
    ang = math.radians(dom)
    if ang > math.pi / 4.0:
        ang -= math.pi / 2.0
    return ang if abs(ang) > 1e-4 else 0.0


def _align_inplane_z(shape):
    """Rotate about Z so the part's DOMINANT edge direction (the orientation
    carrying the most total edge length in the top view, mod 90 deg) becomes
    axis-aligned. Using total length (not a single longest edge) means a plate's
    main rectangular frame wins over an incidental long diagonal/skew feature.

    First, if the top view has no strong rectangular frame but DOES have a regular
    bolt-hole ring, align that ring to the axes instead -- otherwise a round plate
    keeps its holes skewed into an X (it has no straight frame for the histogram
    to lock onto)."""
    top = project(shape, (1, 0, 0), (0, 1, 0), 0.3)   # raw XY projection
    # Collect every straight edge as (angle mod 90, length). Edges 90 deg apart
    # (the two sides of a rectangle) reinforce the same orientation.
    edges = []
    bins = [0.0] * 90
    total = 0.0
    for pl in top["visible"] + top["hidden"]:
        for i in range(len(pl) - 1):
            dx = pl[i + 1][0] - pl[i][0]; dy = pl[i + 1][1] - pl[i][1]
            ln = (dx * dx + dy * dy) ** 0.5
            if ln < 1e-6:
                continue
            a = (math.degrees(math.atan2(dy, dx)) % 90.0)
            edges.append((a, ln))
            bins[int(a) % 90] += ln                # coarse histogram to find peak
            total += ln
    if total < 1e-9:
        return shape
    # Find the dominant orientation to ~1 deg, THEN refine to sub-degree by a
    # length-weighted mean over the ACTUAL edge angles near the peak (the old
    # integer-bin mean left up to ~1 deg of residual skew). Edges straddling the
    # 0/90 wrap are folded so they don't bias the mean.
    peak = max(range(90), key=lambda i: bins[i])
    num = den = 0.0
    for a, ln in edges:
        d = a - peak
        if d > 45.0:
            d -= 90.0
        elif d < -45.0:
            d += 90.0
        if abs(d) <= 5.0:                          # within +/-5 deg of the peak
            num += ln * (peak + d); den += ln
    dom = (num / den) if den else float(peak)      # degrees in [0,90), sub-degree
    # How strongly is the part framed? `den` is the edge length within +/-5 deg of
    # the peak; if it is only a small fraction of all edge length the part has no
    # real rectangular frame (a disc: its outline tessellates into every angle).
    # In that weak case, defer to the bolt-hole ring if there is one, so a round
    # flange's holes land on the axes instead of staying skewed into an X.
    frame_strength = den / total
    if frame_strength < 0.5:
        hole_ang = _hole_pattern_angle(shape)
        if hole_ang is not None:
            ang = hole_ang
        else:
            ang = math.radians(dom)
            if ang > math.pi / 4.0:
                ang -= math.pi / 2.0
    else:
        ang = math.radians(dom)
        if ang > math.pi / 4.0:
            ang -= math.pi / 2.0                  # smallest equivalent rotation
    if abs(ang) < 1e-4:
        return shape
    t = gp_Trsf()
    t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), -ang)
    return BRepBuilderAPI_Transform(shape, t, True).Shape()


def _align_dir_to_z(shape, d):
    """Rotate shape so unit-ish model direction d maps exactly onto +Z."""
    dx, dy, dz = d
    nrm = (dx * dx + dy * dy + dz * dz) ** 0.5
    if nrm < 1e-12:
        return shape
    dx, dy, dz = dx / nrm, dy / nrm, dz / nrm
    if dz > 0.999999:
        return shape                      # already +Z
    t = gp_Trsf()
    if dz < -0.999999:
        # antiparallel: flip 180 about X
        t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi)
    else:
        ax = _cross((dx, dy, dz), (0.0, 0.0, 1.0))   # rotation axis = d x Z
        ang = math.acos(max(-1.0, min(1.0, dz)))
        t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(ax[0], ax[1], ax[2])), ang)
    return BRepBuilderAPI_Transform(shape, t, True).Shape()


def _z_points_up(shape):
    """True if the orientation is acceptable: the volume centroid sits at or
    below the geometric bbox centre in Z (mass-heavy end down). This resolves
    PCA's Z-sign ambiguity uniformly for all parts without assuming regularity."""
    b = Bnd_Box()
    BRepBndLib.Add_s(shape, b)
    xmin, ymin, zmin, xmax, ymax, zmax = b.Get()
    z_centre = 0.5 * (zmin + zmax)
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    z_com = props.CentreOfMass().Z()
    return z_com <= z_centre + 1e-9


def _bbox_dims(shape):
    b = Bnd_Box()
    BRepBndLib.Add_s(shape, b)
    xmin, ymin, zmin, xmax, ymax, zmax = b.Get()
    return (xmax - xmin, ymax - ymin, zmax - zmin)


def circles_for_views(shape):
    """Circular edges that appear as TRUE circles in each standard view (axis
    parallel to the view direction). Returns
        {view: [(radius, cx, cy, is_full, is_hole, cov_turns), ...]}
    where (cx,cy) is the circle centre in that view's (paper_x, paper_y) coords.
      is_full : the edge spans a complete 360-deg circle.
      is_hole : the edge is the mouth of a HOLE/boss (diameter target), as opposed
                to a CORNER FILLET / edge round (radius target). A full circle is
                always a hole. A PARTIAL arc is a hole too when it spans a large
                angle (>~0.6 turn): a hole drilled into a SLOPED or SWEPT face
                projects its mouth as a >180-deg arc, not a full circle -- without
                this it would be mistaken for a fillet and its diameter dropped.
                A small arc (quarter/half round) stays a fillet.
    Holes and fillets can share a radius (R5 fillet vs Ø10 hole both r=5), so the
    caller uses is_hole to tell a DIAMETER target from a RADIUS target.

    CENTRES are the feature's AXIS position (a leader must point at the arc's
    true centre); a cylinder-face centre-of-mass sits INSIDE the material for a
    partial wall (a hole broken out at a corner) and used to drag the callout --
    and every location dimension measured from it -- millimetres off. COVERAGE
    is the union of angular intervals over ALL coaxial entities (edges + wall
    fragments): a boss wall split in two by a slot is still a FULL circle; a
    hole drilled on the part corner keeps only a quarter arc and is reported
    is_full=False, is_hole=False so the caller can dimension it as a RADIUS."""
    HOLE_ARC = 1.2 * math.pi          # >~0.6 turn -> a (possibly clipped) hole mouth
    NBIN = 72                          # 5-deg angular coverage bins
    # ---- collect coaxial candidates in 3D: (r, axis_dir, axis_pnt, pts3d) ----
    cands = []
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge_s(exp.Current())
        c = BRepAdaptor_Curve(edge)
        if c.GetType() == GeomAbs_Circle:
            circ = c.Circle()
            ax = circ.Axis().Direction()
            loc = circ.Location()        # circle centre = a point ON the axis
            cands.append((circ.Radius(), (ax.X(), ax.Y(), ax.Z()),
                          (loc.X(), loc.Y(), loc.Z()),
                          _edge_points3d(edge, deflection=0.05)))
        exp.Next()
    # Cylinder faces: a hole through a SWEPT/curved body has no clean circular
    # mouth edge, but its wall face carries the exact radius+axis. Every boundary
    # point of the wall lies ON the cylinder, so the boundary edges sample the
    # angular coverage directly.
    fexp = TopExp_Explorer(shape, TopAbs_FACE)
    while fexp.More():
        face = TopoDS.Face_s(fexp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            cyl = surf.Cylinder()
            ax = cyl.Axis().Direction()
            loc = cyl.Location()         # a point ON the cylinder axis
            pts = []
            eexp = TopExp_Explorer(face, TopAbs_EDGE)
            while eexp.More():
                pts += _edge_points3d(TopoDS.Edge_s(eexp.Current()),
                                      deflection=0.05)
                eexp.Next()
            if pts:
                cands.append((cyl.Radius(), (ax.X(), ax.Y(), ax.Z()),
                              (loc.X(), loc.Y(), loc.Z()), pts))
        fexp.Next()
    out = {k: [] for k in ("front", "top", "left")}
    for v in out:
        px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
        d = _cross(px, py)               # view direction
        groups = []                       # [r, cx, cy, set(bins)]
        for (r, a, ctr, pts) in cands:
            if abs(a[0]*d[0] + a[1]*d[1] + a[2]*d[2]) <= 0.98:
                continue                  # axis not along this view
            # axis position in view coords (any axis point projects the same)
            cx = ctr[0]*px[0] + ctr[1]*px[1] + ctr[2]*px[2]
            cy = ctr[0]*py[0] + ctr[1]*py[1] + ctr[2]*py[2]
            # angular coverage in the COMMON (paper_x, paper_y) frame: fill the
            # bins each sampled point hits, plus the short arc between
            # consecutive samples (deflection sampling leaves 5-deg holes).
            angs = []
            for p in pts:
                qx = (p[0]*px[0] + p[1]*px[1] + p[2]*px[2]) - cx
                qy = (p[0]*py[0] + p[1]*py[1] + p[2]*py[2]) - cy
                if qx*qx + qy*qy < (0.3 * r) ** 2:
                    continue              # point too near the axis (degenerate)
                angs.append(math.atan2(qy, qx))
            bins = set()
            for ang in angs:
                bins.add(int((ang + math.pi) / (2 * math.pi) * NBIN) % NBIN)
            for a1, a2 in zip(angs, angs[1:]):
                diff = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
                if abs(diff) <= math.radians(40):   # fill the short way only
                    steps = int(abs(diff) / (2 * math.pi) * NBIN) + 1
                    for k in range(1, steps):
                        am = a1 + diff * k / steps
                        bins.add(int((am + math.pi) / (2 * math.pi) * NBIN)
                                 % NBIN)
            if not bins:
                continue
            g = next((gg for gg in groups
                      if abs(gg[0] - r) < 0.05 and abs(gg[1] - cx) < 0.3
                      and abs(gg[2] - cy) < 0.3), None)
            if g is None:
                groups.append([r, cx, cy, bins])
            else:
                g[3] |= bins              # coaxial fragments: union coverage
        for (r, cx, cy, bins) in groups:
            cov = len(bins) / NBIN * 2 * math.pi
            is_full = cov >= 2 * math.pi - 0.30      # allow a couple empty bins
            is_hole = cov >= HOLE_ARC
            # 6th field: coverage in TURNS -- lets the matcher dimension a small
            # leftover arc (corner notch) as R while a half-exposed boss stays Ø.
            out[v].append((round(r, 3), cx, cy, is_full, is_hole,
                           round(cov / (2 * math.pi), 3)))
    return out


def arc_angles_for_views(shape, min_sweep=10.0, max_sweep=350.0,
                         min_radius=4.0, min_arc_len=15.0):
    """SWEPT-ANGLE (张角) of circular-ARC edges that read as a TRUE arc in a
    standard view -- the angular extent of a rotated / arc-swept / sector part.
    Returns {view: [{cx, cy, radius, start_ang, end_ang, sweep_deg,
                     d1, d2}, ...]} where (cx,cy) is the arc CENTRE in that
    view's (paper_x, paper_y) coords, start/end_ang are the arc's endpoint
    angles IN THAT VIEW FRAME (radians), sweep_deg the swept angle (degrees),
    and d1/d2 the two unit RADIUS directions (centre->endpoint) in the view --
    exactly what annotate.angle_dim needs (vertex + two edge directions).

    ISO 129-1 dimensions a body of revolution / arc / sector by its ANGULAR
    extent (an angular dimension, unit degree, symbol °), placed in the view
    where the arc shows its TRUE shape (its plane facing the viewer, i.e. the
    arc axis along the view direction).

    Detection / filtering rationale:
      - Only GeomAbs_Circle edges that are NOT a full turn (sweep < 360-tol):
        a complete circle is a hole/boss handled by circles_for_views, not a
        swept angle.
      - The arc must lie FLAT in the view (its axis ~parallel to the view
        direction) so the projected sweep equals the true sweep; a foreshortened
        arc would mislabel.
      - Reject tiny rounds: radius < min_radius, sweep outside
        [min_sweep, max_sweep], OR arc LENGTH < min_arc_len -- this drops
        fillet/chamfer micro-arcs, near-full circles, and short edge fragments,
        leaving only the part's meaningful arc/sector spans.
      - COLLAPSE one swept feature to ONE callout. An arc-swept band has MANY
        coaxial circular edges -- inner/outer wall rims, top/bottom edges, the
        chamfer/shell rim -- all sharing the SAME CENTRE but at different radii
        and with sweeps clipped to varying sub-spans (83/80/73/45/... on the
        SAME 83-deg band). They are the same feature, so per concentric CENTRE
        we keep ONE representative: the arc with the LARGEST swept angle (the
        true full span), breaking ties by the largest radius (its arc has the
        most room to draw the angle dimension clear). This turns the ~15 raw
        edge fragments of the M6 part into the single meaningful 83-deg张角."""
    out = {k: [] for k in ("front", "top", "left")}
    arcs = []                         # (axis_dir, ctr3d, radius, sweep, p0, p1)
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge_s(exp.Current())
        c = BRepAdaptor_Curve(edge)
        if c.GetType() == GeomAbs_Circle:
            circ = c.Circle()
            r = circ.Radius()
            f = c.FirstParameter(); l = c.LastParameter()
            sweep = math.degrees(abs(l - f))
            # a circular EDGE parameterises directly in radians, so last-first
            # IS the swept angle; a full turn (~360) is a closed circle -> skip.
            # arc LENGTH = r * sweep(rad): drops short edge fragments that share
            # a swept band's centre but only span a few mm.
            arc_len = r * abs(l - f)
            if (r < min_radius or sweep < min_sweep or sweep > max_sweep
                    or arc_len < min_arc_len):
                exp.Next(); continue
            ax = circ.Axis().Direction()
            loc = circ.Location()
            p0 = c.Value(f); p1 = c.Value(l)
            arcs.append(((ax.X(), ax.Y(), ax.Z()),
                         (loc.X(), loc.Y(), loc.Z()), r, sweep,
                         (p0.X(), p0.Y(), p0.Z()), (p1.X(), p1.Y(), p1.Z())))
        exp.Next()
    for v in out:
        px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
        d = _cross(px, py)                       # view direction
        cands = []
        for (a, ctr, r, sweep, p0, p1) in arcs:
            # the arc plane must face the viewer (axis ~ along the view dir),
            # else the projected arc is foreshortened and its angle is wrong.
            if abs(a[0]*d[0] + a[1]*d[1] + a[2]*d[2]) <= 0.98:
                continue
            cx = ctr[0]*px[0] + ctr[1]*px[1] + ctr[2]*px[2]
            cy = ctr[0]*py[0] + ctr[1]*py[1] + ctr[2]*py[2]
            # endpoint directions in the view frame (centre -> arc end)
            e0x = (p0[0]*px[0] + p0[1]*px[1] + p0[2]*px[2]) - cx
            e0y = (p0[0]*py[0] + p0[1]*py[1] + p0[2]*py[2]) - cy
            e1x = (p1[0]*px[0] + p1[1]*px[1] + p1[2]*px[2]) - cx
            e1y = (p1[0]*py[0] + p1[1]*py[1] + p1[2]*py[2]) - cy
            n0 = math.hypot(e0x, e0y); n1 = math.hypot(e1x, e1y)
            if n0 < 1e-6 or n1 < 1e-6:
                continue
            d1 = (e0x / n0, e0y / n0); d2 = (e1x / n1, e1y / n1)
            cands.append({"cx": cx, "cy": cy, "radius": round(r, 3),
                          "start_ang": math.atan2(d1[1], d1[0]),
                          "end_ang": math.atan2(d2[1], d2[0]),
                          "sweep_deg": round(sweep, 1),
                          "d1": d1, "d2": d2})
        if not cands:
            continue
        # DROP small NOTCH / SCALLOP arcs: a tiny R cut on the rim (an R6 scallop
        # on a Ø90 flange) is a RADIUS feature already labelled R, not the part's
        # defining swept angle. Such an arc's radius is a small fraction of the
        # largest arc in the view, so keep only arcs whose radius is >= 0.4x the
        # biggest -- this retains the main outline / swept-band arc(s) and drops
        # the small rim cuts, without a fixed mm threshold that would misjudge
        # small parts.
        rmax = max(c2["radius"] for c2 in cands)
        cands = [c2 for c2 in cands if c2["radius"] >= 0.4 * rmax]
        # COLLAPSE concentric arcs of one swept feature: group by CENTRE (the
        # angle vertex), then keep ONE representative per group -- the largest
        # sweep, ties broken by largest radius. All the inner/outer/rim/chamfer
        # edges of a single arc-swept band share a centre, so this reduces them
        # to the one張角 that describes the band.
        groups = []                              # [list of cand]
        for c2 in cands:
            g = next((gg for gg in groups
                      if abs(gg[0]["cx"] - c2["cx"]) < 1.0
                      and abs(gg[0]["cy"] - c2["cy"]) < 1.0), None)
            if g is None:
                groups.append([c2])
            else:
                g.append(c2)
        for g in groups:
            best = max(g, key=lambda c2: (c2["sweep_deg"], c2["radius"]))
            out[v].append(best)
    return out


def fillet_radii(shape, max_r=15.0):
    """Radii of ROUNDED (fillet/edge-round) SURFACES in the part, with a centre
    in each view. Returns {view: [(radius, cx, cy), ...]}.

    A fillet is a blend surface: a CYLINDER (rounding a straight edge) or a TORUS
    (rounding a curved edge, e.g. the top edge of an arc-swept body). Its radius
    is the cylinder radius / torus MINOR radius. circles_for_views only sees
    circular EDGES that project axis-on as true circles, so a fillet whose edge is
    NOT an axis-aligned circle (a top-edge round, a fillet on a swept/sloped face)
    is invisible there and its R goes unlabelled. Reading the radius off the blend
    SURFACE recovers it. Only small radii (<= max_r) are treated as fillets, so a
    large structural cylinder/bore wall is not mistaken for an edge round.

    The (cx,cy) is the surface's centre-of-mass projected into the view, used to
    anchor the R leader. A surface is offered to a view when its axis is roughly
    parallel to that view direction (so the round reads as an arc there)."""
    out = {k: [] for k in ("front", "top", "left")}
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        t = s.GetType()
        r = axis = None
        if t == GeomAbs_Cylinder:
            r = s.Cylinder().Radius()
            ax = s.Cylinder().Axis().Direction(); axis = (ax.X(), ax.Y(), ax.Z())
        elif t == GeomAbs_Torus:
            r = s.Torus().MinorRadius()
            ax = s.Torus().Axis().Direction(); axis = (ax.X(), ax.Y(), ax.Z())
        if r is None or r > max_r:
            exp.Next(); continue
        props = GProp_GProps(); BRepGProp.SurfaceProperties_s(face, props)
        com = props.CentreOfMass(); ctr = (com.X(), com.Y(), com.Z())
        # face extent = half the bbox diagonal: the face's reach from its centre.
        # Two faces whose centres are within ext1+ext2(+gap) touch -- this is how
        # the caller tells ONE continuous ring of blends (faces chained end to
        # end around an outline) from genuinely separate rounds, so the "n x"
        # counts places, not faces, even when a long edge face's centre is far
        # from its neighbours'.
        fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
        x0, y0, z0, x1, y1, z1 = fb.Get()
        ext = 0.5 * math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
        for v in out:
            px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
            d = _cross(px, py)
            if abs(axis[0]*d[0] + axis[1]*d[1] + axis[2]*d[2]) > 0.85:
                cx = ctr[0]*px[0] + ctr[1]*px[1] + ctr[2]*px[2]
                cy = ctr[0]*py[0] + ctr[1]*py[1] + ctr[2]*py[2]
                out[v].append((round(r, 3), cx, cy, round(ext, 2)))
        exp.Next()
    # de-dup near-identical (radius, centre) per view
    for v in out:
        uniq = []
        for r, cx, cy, ext in out[v]:
            if not any(abs(r - r2) < 0.05 and abs(cx - x2) < 0.5
                       and abs(cy - y2) < 0.5 for r2, x2, y2, _e2 in uniq):
                uniq.append((r, cx, cy, ext))
        out[v] = uniq
    return out


def chamfer_sizes(shape, max_size=10.0):
    """Chamfer sizes read off CONE faces, with a centre in each view.
    Returns {view: [(size, cx, cy), ...]}.

    Chamfering a CIRCULAR edge (the rim of a disc/boss/hole) produces a CONE
    face, not a flat slant -- so _chamfer_edges (which hunts 45-deg straight
    segments) cannot see it, and on a round part the rim chamfer projects a
    foreshortened leg (0.5-0.7 of its true size) that never matches the nominal
    value. The cone carries the exact size: for a chamfer of leg c at semi-angle
    a, the cone's axial height h relates as size = h/cos? -- for the common 45-deg
    chamfer the axial height EQUALS the chamfer distance, and more generally
    size = h / tan(pi/2 - semiangle) reduces to h for 45 deg. We report the cone's
    axial extent, which equals the chamfer leg for the dominant 45-deg case.

    Anchored at the cone centre-of-mass projected into each view whose direction
    is roughly along the cone axis (so the chamfer reads as a thin rim there)."""
    out = {k: [] for k in ("front", "top", "left")}
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        if s.GetType() == GeomAbs_Cone:
            cone = s.Cone()
            ax = cone.Axis().Direction(); axis = (ax.X(), ax.Y(), ax.Z())
            # axial height of this cone face = chamfer leg (exact for 45 deg)
            fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
            x0, y0, z0, x1, y1, z1 = fb.Get()
            # project the face's bbox diagonal onto the cone axis for the height
            diag = (x1 - x0, y1 - y0, z1 - z0)
            height = abs(diag[0]*axis[0] + diag[1]*axis[1] + diag[2]*axis[2])
            size = height
            if size <= 1e-3 or size > max_size:
                exp.Next(); continue
            props = GProp_GProps(); BRepGProp.SurfaceProperties_s(face, props)
            com = props.CentreOfMass(); ctr = (com.X(), com.Y(), com.Z())
            for v in out:
                px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
                d = _cross(px, py)
                if abs(axis[0]*d[0] + axis[1]*d[1] + axis[2]*d[2]) > 0.85:
                    cx = ctr[0]*px[0] + ctr[1]*px[1] + ctr[2]*px[2]
                    cy = ctr[0]*py[0] + ctr[1]*py[1] + ctr[2]*py[2]
                    out[v].append((round(size, 3), cx, cy))
        exp.Next()
    for v in out:
        uniq = []
        for sz, cx, cy in out[v]:
            if not any(abs(sz - s2) < 0.05 and abs(cx - x2) < 0.5
                       and abs(cy - y2) < 0.5 for s2, x2, y2 in uniq):
                uniq.append((sz, cx, cy))
        out[v] = uniq
    return out


def chamfer_bevels(shape, max_size=10.0):
    """Chamfer sizes read off flat SLANTED bevel PLANES, with a centre in each
    view. Returns {view: [(size, cx, cy), ...]}.

    Chamfering a STRAIGHT edge (the rim of a rectangular boss/pocket/rib, a slot
    mouth) makes a flat slanted strip, NOT a cone -- so chamfer_sizes (cone-only)
    misses it, and the parameter matcher's _chamfer_edges deliberately rejects
    internal slants that aren't on an OUTER corner (to avoid mislabeling). That
    leaves the chamfer of an INTERNAL feature (a boss/pocket rim away from the
    outline) unlabelled. This reads the leg straight off the bevel face so those
    inner chamfers get their C.

    A bevel is a small planar face whose normal is TILTED (~30-60 deg) off every
    principal axis -- neither a flat top/bottom (n//Z) nor an upright wall
    (n.Z~0). For a 45-deg chamfer of leg c the strip is thin across one axis and
    long along the edge it cuts; the chamfer leg equals the strip's SMALLEST
    axis-aligned bbox span (a leg-c 45-deg bevel rises c in each of the two
    perpendicular directions, so each per-axis extent across the strip is c).
    Only small legs (<= max_size) are treated as chamfers.

    Anchored at the bevel centre-of-mass projected into each view whose direction
    is roughly along the bevel-strip RUN (so it reads as a thin line there)."""
    out = {k: [] for k in ("front", "top", "left")}
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        if s.GetType() == GeomAbs_Plane:
            n = s.Plane().Axis().Direction()
            nz = abs(n.Z())
            nh = math.hypot(n.X(), n.Y())          # in-plane (horizontal) component
            # a bevel normal is tilted off BOTH vertical and horizontal: 0.20 < nz
            # < 0.98 with a real horizontal part rules out flat faces (nz~1) and
            # upright walls (nz~0).
            size = None
            top_ok = False
            if 0.20 < nz < 0.98 and nh > 0.10:
                fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
                x0, y0, z0, x1, y1, z1 = fb.Get()
                spans = sorted([x1 - x0, y1 - y0, z1 - z0])
                size = spans[0]                    # smallest span = 45-deg leg
            elif nz <= 0.20 and nh > 1e-6 \
                    and min(abs(n.X()), abs(n.Y())) > 0.40 * nh:
                # VERTICAL-EDGE chamfer: chamfering an UPRIGHT edge leaves an
                # upright bevel strip whose normal is HORIZONTAL but DIAGONAL
                # (tilted off both the X and Y walls) -- the nz-window above
                # can never see it, which left every vertical chamfer bare.
                # Leg = the horizontal bbox spans (equal for a 45-deg cut;
                # nominal = the larger leg for an asymmetric one).
                fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
                x0, y0, z0, x1, y1, z1 = fb.Get()
                size = max(x1 - x0, y1 - y0)
                # a FEATURE WALL that the pose left diagonal (a slot wall in a
                # rotated ring) passes the normal test too; a real vertical
                # chamfer is a NARROW strip, so cap the leg tightly -- better
                # to leave an unusually large corner cut to the outline dims
                # than to stamp a wall with a bogus C.
                if size > 3.0:
                    size = None
                top_ok = True   # TOP shows the cut as its true 45-deg corner line
            if size is not None and 1e-2 < size <= max_size:
                props = GProp_GProps()
                BRepGProp.SurfaceProperties_s(face, props)
                com = props.CentreOfMass()
                ctr = (com.X(), com.Y(), com.Z())
                # offer to a view when the bevel reads as a thin rim there:
                # its normal has a strong component along that view direction.
                # face extent = half bbox diagonal -- see fillet_radii: lets
                # the caller chain end-to-end faces of one continuous ring
                # chamfer into a single counted place.
                ext = 0.5 * math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
                for v in out:
                    px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
                    d = _cross(px, py)
                    ndotd = abs(n.X()*d[0] + n.Y()*d[1] + n.Z()*d[2])
                    if ndotd > 0.45 or (top_ok and v == "top"):
                        cx = ctr[0]*px[0] + ctr[1]*px[1] + ctr[2]*px[2]
                        cy = ctr[0]*py[0] + ctr[1]*py[1] + ctr[2]*py[2]
                        out[v].append((round(size, 3), cx, cy,
                                       round(ext, 2)))
        exp.Next()
    for v in out:
        uniq = []
        for sz, cx, cy, ext in out[v]:
            if not any(abs(sz - s2) < 0.1 and abs(cx - x2) < 0.6
                       and abs(cy - y2) < 0.6 for s2, x2, y2, _e2 in uniq):
                uniq.append((sz, cx, cy, ext))
        out[v] = uniq
    return out


def rect_features(shape, min_size=2.0):
    """Rectangular POCKET / BOSS / RIB footprints, with a centre, per view.
    Returns {view: [(w, h, cx, cy), ...]} where (w,h) are the footprint extents
    in that view's (paper_x, paper_y) and (cx,cy) the centre.

    A pocket floor / boss top / rib top is a HORIZONTAL planar face (n//Z) that
    sits at a Z DISTINCT from the part's main top & bottom faces -- recessed
    (pocket) or raised (boss/rib). Such a feature's own W x H size is not a named
    outline dimension and the parameter matcher often misses it (a pocket's depth
    axis isn't the Z its name implies), so the rectangle reads UNDIMENSIONED. We
    read the footprint straight off the face bbox so it can be dimensioned.

    Only the dominant in-plane projection is offered (TOP for a Z-stacked feature),
    where the rectangle is true-size. Tiny faces (< min_size) are skipped."""
    out = {k: [] for k in ("front", "top", "left")}
    # find the part's main top & bottom Z (largest-area horizontal faces) so we
    # can tell a feature face (different Z) from the base surfaces.
    gb = Bnd_Box(); BRepBndLib.Add_s(shape, gb)
    gx0, gy0, gz0, gx1, gy1, gz1 = gb.Get()
    part_w = gx1 - gx0; part_d = gy1 - gy0
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    horiz = []                                     # (z, area, w_x, w_y, cx, cy)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        if s.GetType() == GeomAbs_Plane:
            n = s.Plane().Axis().Direction()
            if abs(n.Z()) > 0.98:
                props = GProp_GProps(); BRepGProp.SurfaceProperties_s(face, props)
                com = props.CentreOfMass(); area = props.Mass()
                fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
                x0, y0, z0, x1, y1, z1 = fb.Get()
                horiz.append((com.Z(), area, x1 - x0, y1 - y0, com.X(), com.Y()))
        exp.Next()
    if not horiz:
        return out
    # The part's main top/bottom SURFACES are the large-area horizontal faces; a
    # rib/boss can split the top into fragments that no longer touch the global
    # Z extremes, so identifying base by Z alone is not enough. Treat any large
    # horizontal face (>= 60% of the biggest) OR one at the global top/bottom Z as
    # a base surface, never a feature. A real pocket floor / boss top is a SMALL
    # face at an intermediate Z.
    max_area = max(a for (_z, a, _wx, _wy, _cx, _cy) in horiz)

    def _is_base(z, area):
        if area >= 0.60 * max_area:
            return True
        return abs(z - gz0) < 0.2 or abs(z - gz1) < 0.2
    for (z, area, wx, wy, cx, cy) in horiz:
        if _is_base(z, area):
            continue                               # the part's own top/bottom
        if wx < min_size or wy < min_size:
            continue
        if area < min_size * min_size:
            continue
        # a face spanning most of the part in EITHER direction is a surface
        # fragment / full-width shelf (the top split by a rib, a tray's inner
        # ledge), not a discrete pocket/boss. Require the feature to be LOCALIZED:
        # under 80% of the part in both X and Y. This keeps real pockets/bosses and
        # drops full-span strips that would read as noise.
        if wx >= 0.80 * part_w or wy >= 0.80 * part_d:
            continue
        # footprint is rectangular if it nearly fills its bbox (area ~ wx*wy);
        # a round/irregular recess fails this and is left to circle/other paths.
        if area < 0.75 * wx * wy:
            continue
        # an INTERIOR feature only: a face FLUSH with the part's outline on ANY
        # side (a wall/rim top face, an L-leg's riser top, a corner pad) is part
        # of the silhouette -- its extents are outline dimensions, already the
        # matcher's job -- and dimensioning its W x H doubles up as a floating,
        # meaningless number. A true pocket/boss is surrounded by material, so
        # require clearance to the part bbox on ALL four sides.
        margin = 0.5
        x_lo, x_hi = cx - wx / 2, cx + wx / 2
        y_lo, y_hi = cy - wy / 2, cy + wy / 2
        if (x_lo - gx0 < margin or gx1 - x_hi < margin
                or y_lo - gy0 < margin or gy1 - y_hi < margin):
            continue                               # flush with the outline
        # offer to TOP (Z-stacked feature reads true-size from above), projected
        # into that view's PAPER axes -- raw model coords drew the rectangle
        # mirrored/outside the view when an axis flips sign in the projection.
        px = VIEWS["top"]["paper_x"]; py = VIEWS["top"]["paper_y"]
        pcx = cx * px[0] + cy * px[1] + z * px[2]
        pcy = cx * py[0] + cy * py[1] + z * py[2]
        pw = abs(wx * px[0]) + abs(wy * px[1])     # extent along paper_x
        ph = abs(wx * py[0]) + abs(wy * py[1])     # extent along paper_y
        out["top"].append((round(pw, 2), round(ph, 2), pcx, pcy))
    # de-dup near-identical footprints (a pocket floor + its rim can both appear)
    for v in out:
        uniq = []
        for (w, h, cx, cy) in out[v]:
            if not any(abs(w - w2) < 0.5 and abs(h - h2) < 0.5
                       and abs(cx - x2) < 0.6 and abs(cy - y2) < 0.6
                       for (w2, h2, x2, y2) in uniq):
                uniq.append((w, h, cx, cy))
        out[v] = uniq
    return out


def wall_gap_dims(shape, min_gap=1.5, max_pairs=24):
    """Distances between OPPOSING INTERIOR axis-aligned planar walls -- the
    width/length of through-slots, cavities and channels. rect_features needs a
    pocket FLOOR (a horizontal face at intermediate Z); a slot CUT CLEAN THROUGH
    the part has none, so its footprint went undimensioned. The two bounding
    WALL faces always exist, and the gap between them IS the feature size.

    Returns {view: [(gap, (x0,y0,x1,y1), axis), ...]} where the edge is in that
    view's paper coords (same raw dot-product frame as project()) and axis is
    the model axis ('x'|'y'|'z') the gap is measured along. Each interior wall
    is paired with its NEAREST opposing neighbour that overlaps it in BOTH
    transverse directions, so nested features pair wall-to-facing-wall, never
    across an intervening web."""
    gb = Bnd_Box(); BRepBndLib.Add_s(shape, gb)
    gx0, gy0, gz0, gx1, gy1, gz1 = gb.Get()
    lo = {"x": gx0, "y": gy0, "z": gz0}
    hi = {"x": gx1, "y": gy1, "z": gz1}
    walls = {"x": [], "y": [], "z": []}    # axis -> (coord, b_lo, b_hi) bboxes
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        if s.GetType() == GeomAbs_Plane:
            n = s.Plane().Axis().Direction()
            nv = (n.X(), n.Y(), n.Z())
            axis = next((ax for i, ax in enumerate("xyz")
                         if abs(nv[i]) > 0.98), None)
            if axis is not None:
                fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
                b = fb.Get()               # (x0,y0,z0,x1,y1,z1)
                i = "xyz".index(axis)
                coord = (b[i] + b[i + 3]) / 2.0
                # INTERIOR only: a wall on the part outline is a silhouette
                # face -- its position is an outline dimension, not a feature.
                if coord - lo[axis] < 0.5 or hi[axis] - coord < 0.5:
                    exp.Next(); continue
                walls[axis].append((coord, b))
        exp.Next()
    # merge fragments of the same wall plane (a slot wall broken by a boss):
    # same axis+coord -> union their transverse extents.
    for axis in walls:
        walls[axis].sort(key=lambda w: w[0])
        merged = []
        for (c, b) in walls[axis]:
            m = next((mm for mm in merged if abs(mm[0] - c) < 0.10), None)
            if m is None:
                merged.append([c, list(b)])
            else:
                m[1] = [min(m[1][k], b[k]) for k in range(3)] + \
                       [max(m[1][k + 3], b[k + 3]) for k in range(3)]
        walls[axis] = merged
    # views where a gap along each model axis reads TRUE SIZE, with that view's
    # paper axes (project() emits raw dot products, so the same math lines up).
    AXIS_VIEW = {"x": "top", "y": "top", "z": "front"}
    out = {k: [] for k in ("front", "top", "left")}
    for axis, ws in walls.items():
        i = "xyz".index(axis)
        t1, t2 = [k for k in range(3) if k != i]   # transverse axis indices
        view = AXIS_VIEW[axis]
        px = VIEWS[view]["paper_x"]; py = VIEWS[view]["paper_y"]
        n_pairs = 0
        for a_i in range(len(ws)):
            if n_pairs >= max_pairs:
                break
            ca, ba = ws[a_i]
            for b_i in range(a_i + 1, len(ws)):    # nearest neighbour upward
                cb, bb = ws[b_i]
                gap = cb - ca
                if gap < min_gap:
                    continue
                # require overlap in BOTH transverse directions (facing walls)
                o1 = min(ba[t1 + 3], bb[t1 + 3]) - max(ba[t1], bb[t1])
                o2 = min(ba[t2 + 3], bb[t2 + 3]) - max(ba[t2], bb[t2])
                if o1 < 1.0 or o2 < 1.0:
                    continue
                # edge endpoints: across the gap at the overlap-band midpoint
                mid = [0.0, 0.0, 0.0]
                mid[t1] = (max(ba[t1], bb[t1]) + min(ba[t1 + 3], bb[t1 + 3])) / 2
                mid[t2] = (max(ba[t2], bb[t2]) + min(ba[t2 + 3], bb[t2 + 3])) / 2
                p0 = list(mid); p0[i] = ca
                p1 = list(mid); p1[i] = cb
                e = (p0[0]*px[0] + p0[1]*px[1] + p0[2]*px[2],
                     p0[0]*py[0] + p0[1]*py[1] + p0[2]*py[2],
                     p1[0]*px[0] + p1[1]*px[1] + p1[2]*px[2],
                     p1[0]*py[0] + p1[1]*py[1] + p1[2]*py[2])
                out[view].append((round(gap, 2), e, axis))
                n_pairs += 1
                break                              # nearest opposing wall only
    return out


def _discretize_edge(edge, deflection=0.05):
    """Return list of (x,y) points approximating a (already projected, planar) edge."""
    curve = BRepAdaptor_Curve(edge)
    try:
        gc = GCPnts_QuasiUniformDeflection(curve, deflection)
    except Exception:
        return []
    pts = []
    if gc.IsDone():
        for i in range(1, gc.NbPoints() + 1):
            p = gc.Value(i)
            pts.append((p.X(), p.Y()))
    return pts


def _edges_to_polylines(shape, deflection=0.05):
    """Walk all edges of a 2D HLR-result shape -> list of polylines [(x,y),...]."""
    polylines = []
    if shape is None:
        return polylines
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge_s(exp.Current())
        pts = _discretize_edge(edge, deflection)
        if len(pts) >= 2:
            polylines.append(pts)
        exp.Next()
    return polylines


def _cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def project(shape, paper_x, paper_y, deflection=0.05):
    """
    Project `shape` onto a plane defined by EXPLICIT paper axes (in model coords).
    paper_x: model direction that maps to drawing-X (rightward).
    paper_y: model direction that maps to drawing-Y (upward).
    This pins the in-plane orientation so first-angle views stay mutually aligned
    (FRONT and TOP share +X; FRONT and LEFT share +Z), avoiding flipped views.
    """
    # The VIEWER must sit on the +(paper_x x paper_y) side and look toward the
    # part, so that the face we name (top/front/...) shows as VISIBLE edges.
    # OCC's projector views along -normal, so set normal = -(paper_x x paper_y);
    # that flip inverts the in-plane Y, which we undo by negating output Y.
    zc = _cross(paper_x, paper_y)
    z = gp_Dir(-zc[0], -zc[1], -zc[2])
    x = gp_Dir(paper_x[0], paper_x[1], paper_x[2])
    ax2 = gp_Ax2(gp_Pnt(0, 0, 0), z, x)
    projector = HLRAlgo_Projector(ax2)

    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(projector)
    algo.Update()
    algo.Hide()

    hlr = HLRBRep_HLRToShape(algo)
    visible = []
    hidden = []
    for getter in ("VCompound", "Rg1LineVCompound", "OutLineVCompound"):
        try:
            comp = getattr(hlr, getter)()
            visible += _edges_to_polylines(comp, deflection)
        except Exception:
            pass
    for getter in ("HCompound", "Rg1LineHCompound", "OutLineHCompound"):
        try:
            comp = getattr(hlr, getter)()
            hidden += _edges_to_polylines(comp, deflection)
        except Exception:
            pass
    # undo the Y inversion caused by flipping the projector normal
    visible = [[(x_, -y_) for (x_, y_) in pl] for pl in visible]
    hidden = [[(x_, -y_) for (x_, y_) in pl] for pl in hidden]
    return {"visible": visible, "hidden": hidden}


def _perp_x(z_dir, up_dir):
    """Build an X direction perpendicular to z given an up hint, return gp_Dir."""
    zx, zy, zz = z_dir.X(), z_dir.Y(), z_dir.Z()
    ux, uy, uz = up_dir.X(), up_dir.Y(), up_dir.Z()
    # x = up cross z
    cx = uy * zz - uz * zy
    cy = uz * zx - ux * zz
    cz = ux * zy - uy * zx
    n = math.sqrt(cx * cx + cy * cy + cz * cz)
    if n < 1e-9:
        # up parallel to z; pick arbitrary
        return gp_Dir(1, 0, 0)
    return gp_Dir(cx / n, cy / n, cz / n)


def bbox_of_polylines(views):
    xs, ys = [], []
    for v in views:
        for pl in v["visible"] + v["hidden"]:
            for (x, y) in pl:
                xs.append(x); ys.append(y)
    if not xs:
        return (0, 0, 0, 0)
    return (min(xs), min(ys), max(xs), max(ys))


# View definitions by EXPLICIT paper axes in model coords (X=length, Y=depth,
# Z=height). First-angle requires shared axes between adjacent views:
#   FRONT & TOP share drawing-X (= model +X)  -> features line up vertically
#   FRONT & LEFT share drawing-Y (= model +Z) -> features line up horizontally
# Each view: (paper_x, paper_y). View direction is derived as paper_x x paper_y.
VIEWS = {
    # FRONT: X right, Z up
    "front": dict(paper_x=(1, 0, 0), paper_y=(0, 0, 1)),
    # TOP (placed BELOW front): X right, depth(-Y) up so it aligns with front
    "top":   dict(paper_x=(1, 0, 0), paper_y=(0, -1, 0)),
    # LEFT (placed RIGHT of front): depth(Y) right, Z up
    "left":  dict(paper_x=(0, 1, 0), paper_y=(0, 0, 1)),
    # ISO: isometric pictorial
    "iso":   dict(paper_x=(1, -1, 0), paper_y=(-1, -1, 2)),
}


# ===========================================================================
# SWEEP PATH extraction (formerly sweep_path.py)
#
# A swept feature is built by moving a profile along a PATH (a wire). The path is
# the feature's spine; ISO drawings show it as a CENTRELINE (dash-dot) and tag
# its key dimensions (overall length, arc radii, helix pitch).
#
# The path wire is recovered from the build script (it is always a named variable
# passed to `.sweep(<var>)`), then posed IDENTICALLY to the model by fusing it
# with the result solid into one compound and running that compound through
# normalize_pose (a non-solid wire does not perturb the volume/OBB-based pose,
# verified empirically). The posed path is then projected into each view with the
# same paper_x/paper_y mapping used above, so it overlays the views exactly.
# ===========================================================================

_SWEEP_ARG = re.compile(r"\.sweep\(\s*([A-Za-z_]\w*)")
# The LHS variable of a `<lhs> = <...>.sweep(<path>)` statement: the swept solid.
# LHS variable of `<lhs> = ... .sweep(...)`. Two forms occur in the dataset:
#   single line:  swept = wp.circle(r).sweep(path)
#   multi-line chain:  swept = (\n  wp\n  .circle(r)\n  .sweep(path)\n)
# A single-line regex misses the multi-line chain (the `.sweep(` sits several
# lines below the `swept =`), so the swept variable -- and a DEGENERATE zero-volume
# sweep -- went undetected and its phantom path got drawn. Match BOTH: capture the
# LHS of any assignment whose right-hand side (up to the next top-level statement)
# contains a `.sweep(`.
_SWEEP_LHS = re.compile(
    r"^([A-Za-z_]\w*)\s*=\s*(?:\([^=]*?\.sweep\(|[^\n=]*\.sweep\()",
    re.M | re.S)


def _sweep_assignment_names(src):
    """Names of variables assigned a value built with `.sweep(...)`, robust to
    multi-line parenthesised chains. Walks each top-level `name =` and, balancing
    parentheses, checks whether the assigned expression contains a `.sweep(`."""
    names = []
    lines = src.splitlines()
    assign = re.compile(r"^([A-Za-z_]\w*)\s*=")
    for i, line in enumerate(lines):
        ma = assign.match(line)
        if not ma:
            continue
        # accumulate the RHS across continuation lines by paren balance
        chunk = line[ma.end():]
        depth = chunk.count("(") - chunk.count(")")
        j = i
        while depth > 0 and j + 1 < len(lines):
            j += 1
            chunk += "\n" + lines[j]
            depth += lines[j].count("(") - lines[j].count(")")
        if ".sweep(" in chunk:
            names.append(ma.group(1))
    return names


def _solid_volume(obj):
    """Volume of a cadquery Workplane / Shape, 0.0 on any failure."""
    try:
        v = obj.val() if hasattr(obj, "val") else obj
        return v.Volume()
    except Exception:
        return 0.0


def _reexec(folder):
    """Run the build script; return (result_occ_shape, path_occ_shape) or
    (None, None). Both are raw OCP TopoDS shapes.

    Returns (None, None) when the sweep is DEGENERATE: some dataset scripts call
    .sweep() on a profile whose plane is parallel to the path tangent, so OCCT
    produces a zero-volume (collapsed) swept solid. That solid contributes no
    material to `result`, yet the path wire still exists -- drawing its centreline
    would float a dash-dot curve over empty space (no feature is actually there).
    Detecting volume<=0 on the swept variable lets the caller skip the path."""
    path = os.path.join(folder, "cadquery.py")
    src = open(path, encoding="utf-8").read()
    m = _SWEEP_ARG.search(src)
    if not m:
        return None, None
    ns = {"cq": cq, "math": math}
    try:
        exec(src, ns)
    except Exception:
        return None, None
    res = ns.get("result")
    pth = ns.get(m.group(1))
    if res is None or pth is None:
        return None, None
    # Reject degenerate sweeps: every swept solid in the script must have volume.
    # Two layers: (a) the named LHS of each sweep assignment (handles single- and
    # multi-line chains), and (b) a namespace-wide safety net -- ANY cadquery
    # solid variable that collapsed to ~zero volume signals a failed sweep on this
    # part, so its path is phantom and must not be drawn. (b) catches odd
    # assignment styles the regex cannot, which previously let a zero-volume swept
    # body through and floated an R-arc centreline over a flat plate.
    for lhs in set(_SWEEP_LHS.findall(src)):
        if lhs in ns and _solid_volume(ns[lhs]) <= 1e-6:
            return None, None
    # Safety net: the swept profile var (`.circle(r).sweep(path)` assigned to some
    # name) must yield a 3D body. If the result of any `.sweep(` chain collapsed
    # (OCCT returns a zero-area-thickness shell when the profile plane is parallel
    # to the path tangent), the swept feature does not exist -> phantom path. Find
    # every line that ASSIGNS something built with .sweep and re-check by value.
    for nm in _sweep_assignment_names(src):
        if nm in ns and _solid_volume(ns[nm]) <= 1e-6:
            return None, None
    if hasattr(res, "val"):
        res = res.val()
    if hasattr(pth, "val"):
        pth = pth.val()
    try:
        wpth = pth.wrapped
    except Exception:
        return None, None
    # Reject a CLOSED-LOOP path (a profile swept a full turn around a circle ->
    # a body of REVOLUTION, e.g. a bellows/ring). Its "path" is a complete circle;
    # a centreline tracing it is meaningless, and re-exec'd revolution geometry
    # (filleted/cut) makes HLR projection diverge. Drawing such a part from the
    # clean STEP solid + plain inner/outer-diameter dims is correct, so signal
    # "not a drawable sweep path" by returning None.
    if _path_is_closed_loop(wpth):
        return None, None
    try:
        return res.wrapped, wpth
    except Exception:
        return None, None


def _path_is_closed_loop(wire_or_edge):
    """True if the sweep path forms a closed loop -- a single full-circle edge
    (360-degree span) or a wire whose start and end coincide. Such a path winds
    a profile all the way around (a revolution/ring), so it is not a centreline-
    drawable spine."""
    edges = []
    ex = TopExp_Explorer(wire_or_edge, TopAbs_EDGE)
    while ex.More():
        edges.append(TopoDS.Edge_s(ex.Current()))
        ex.Next()
    if not edges:
        return False
    # single full-circle edge -> closed
    if len(edges) == 1:
        c = BRepAdaptor_Curve(edges[0])
        if c.GetType() == GeomAbs_Circle:
            span = abs(c.LastParameter() - c.FirstParameter())
            if span >= 2 * math.pi - 0.05:
                return True
    # otherwise: do the wire's two endpoints coincide?
    vs = []
    vx = TopExp_Explorer(wire_or_edge, TopAbs_VERTEX)
    seen = set()
    while vx.More():
        v = vx.Current()
        p = BRep_Tool.Pnt_s(TopoDS.Vertex_s(v))
        key = (round(p.X(), 4), round(p.Y(), 4), round(p.Z(), 4))
        if key not in seen:
            seen.add(key)
            vs.append(p)
        vx.Next()
    # a closed wire visits each interior vertex twice -> few UNIQUE vertices
    # relative to edge count; an open polyline has edges+1 unique vertices.
    if len(edges) >= 2 and len(vs) <= len(edges):
        return True
    return False


def posed_solid_and_path(folder):
    """Re-exec the build script, fuse the result SOLID and the swept PATH wire
    into one compound, and pose THAT compound once. Return
        (posed_solid, [posed path edges])
    so the caller can project the SAME posed solid for the views AND draw the
    SAME posed path as a centreline -> they are guaranteed aligned (they share
    one pose). Returns (None, []) for non-swept parts or on failure.

    This is the crux of correctness: posing the re-exec solid and the STEP solid
    SEPARATELY gives slightly different poses (OBB axis sign/order is ambiguous
    for near-symmetric parts), so the path drawn from a separate pose never lines
    up. Sharing one pose for both removes that mismatch entirely."""
    res, pth = _reexec(folder)
    if res is None:
        return None, []
    comp = TopoDS_Compound()
    b = BRep_Builder()
    b.MakeCompound(comp)
    b.Add(comp, res)
    b.Add(comp, pth)
    try:
        posed = normalize_pose(comp)
    except Exception:
        return None, []
    # Split the posed compound back into its SOLID (for views) and the free wire
    # edges (the path). Path edges are those bounding NO face of the solid.
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.TopExp import TopExp
    from OCP.TopTools import (TopTools_IndexedDataMapOfShapeListOfShape,
                              TopTools_IndexedMapOfShape)
    # extract the solid (first solid in the posed compound)
    sx = TopExp_Explorer(posed, TopAbs_SOLID)
    posed_solid = TopoDS.Solid_s(sx.Current()) if sx.More() else posed
    edge_face = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(posed, TopAbs_EDGE, TopAbs_FACE, edge_face)
    emap = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(posed, TopAbs_EDGE, emap)
    free = []
    for i in range(1, emap.Extent() + 1):
        e = TopoDS.Edge_s(emap.FindKey(i))
        try:
            nfaces = edge_face.FindFromKey(e).Extent()
        except Exception:
            nfaces = 0
        if nfaces == 0:               # free edge = part of the path wire
            free.append(e)
    return posed_solid, free


# How far a path point may sit OUTSIDE the solid surface and still be drawn.
# A centreline correctly extends a small overshoot past the feature's end face
# (ISO convention), so a few mm is right; points further out are phantom path
# (an elbow arc's far half with no pipe, an over-long helix tail) and dropped.
# The inside-the-bore case is handled separately (those points test as INSIDE
# via the solid classifier, so tolerance does not apply to them).
_CLIP_TOL = 3.0


def _point_keeper(clip_solid):
    """Return (keep, inside): two predicates over (x,y,z).
      keep   -> point is inside the solid OR within _CLIP_TOL of its surface
                (used to assemble the drawn run, allowing a small ISO overshoot).
      inside -> point is strictly inside-or-on the material (dist ~ 0); used to
                trim the run's ENDS so the centreline finishes at the feature
                boundary instead of spilling a tail of barely-in-tolerance points
                out into empty space (e.g. an arc-swept boss whose path arc
                continues past the base plate).
    With no solid (or on failure) both keep-all."""
    if clip_solid is None:
        allow = lambda x, y, z: True
        return allow, allow
    try:
        from OCP.BRepClass3d import BRepClass3d_SolidClassifier
        from OCP.TopAbs import TopAbs_OUT
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        cls = BRepClass3d_SolidClassifier(clip_solid)

        def _dist_out(x, y, z):
            p = gp_Pnt(x, y, z)
            cls.Perform(p, 1e-6)
            if cls.State() != TopAbs_OUT:
                return 0.0                 # inside the material
            v = BRepBuilderAPI_MakeVertex(p).Vertex()
            return BRepExtrema_DistShapeShape(v, clip_solid).Value()

        def keep(x, y, z):
            return _dist_out(x, y, z) <= _CLIP_TOL

        def inside(x, y, z):
            return _dist_out(x, y, z) <= 0.5   # essentially on/in the material
        return keep, inside
    except Exception:
        allow = lambda x, y, z: True
        return allow, allow


def _trim_to_solid(pts, keep, inside=None):
    """Keep the LONGEST CONTIGUOUS run of in-feature points (a path that dips out
    of the solid and back must not bridge the gap into a false chord, so only one
    unbroken segment is returned). Then, if `inside` is given, trim the run's two
    ENDS back to the last point that is actually inside the material plus ONE
    overshoot point -- so the centreline stops at the feature boundary with the
    small ISO overshoot, not a long tail of just-in-tolerance points pointing
    into empty space."""
    if not pts:
        return pts
    best = cur = []
    for p in pts:
        if keep(*p):
            cur = cur + [p]
            if len(cur) > len(best):
                best = cur
        else:
            cur = []
    if inside is None or not best:
        return best
    flags = [inside(*p) for p in best]
    if not any(flags):
        return best
    lo = flags.index(True)
    hi = len(flags) - 1 - flags[::-1].index(True)
    lo = max(0, lo - 1)                     # keep one overshoot point each side
    hi = min(len(best) - 1, hi + 1)
    return best[lo:hi + 1]


def _discretize_path(edge, deflection=0.25, min_pts=64):
    """Sample points along an edge. Try deflection-based sampling first; if it
    yields too few points (BSpline/helix curves often collapse to 2), fall back
    to uniform sampling by curve parameter so helixes/splines are captured."""
    c = BRepAdaptor_Curve(edge)
    pts = []
    try:
        gc = GCPnts_QuasiUniformDeflection(c, deflection)
        if gc.IsDone():
            for i in range(1, gc.NbPoints() + 1):
                p = gc.Value(i)
                pts.append((p.X(), p.Y(), p.Z()))
    except Exception:
        pass
    if len(pts) < min_pts:
        # uniform-by-parameter fallback (robust for curved spines)
        try:
            t0, t1 = c.FirstParameter(), c.LastParameter()
            n = max(min_pts, 64)
            pts = []
            for k in range(n + 1):
                t = t0 + (t1 - t0) * k / n
                p = c.Value(t)
                pts.append((p.X(), p.Y(), p.Z()))
        except Exception:
            pass
    return pts


def describe_edges(edges, clip_solid=None):
    """Build the path-description dict from a list of already-posed OCP edges:
        {'edges3d': [{'pts3d':[(x,y,z)...], 'kind':'line'|'arc'|'helix'|'curve',
                      'radius':r or None, 'length':L}, ...],
         'length': total path length (mm), 'pitch': helix pitch (mm) or None}
    All coords are in the POSED (drawing) model frame. Returns None if empty.

    Clipping: a centreline must only be drawn where the FEATURE IT DESCRIBES
    actually exists. Several cadquery models build a path that is LONGER than the
    fabricated part (e.g. a 180-degree elbow arc whose far half has no pipe on it
    once the flange/stub cut the tube back; or makeHelix building a wire taller
    than the threaded region). Drawing the full path then floats a centreline in
    empty space outside the model silhouette.

    `clip_solid` = the posed SOLID. When given, each discretized point is kept
    only if it lies INSIDE the solid or within `_CLIP_TOL` mm of its surface --
    so the centreline of a hollow bore (the point is in the empty bore but close
    to the wall) is kept, while points floating far outside the body are dropped.
    Length/pitch are reported from the FULL edge (intrinsic; not affected by the
    drawn extent)."""
    if not edges:
        return None
    keep, inside = _point_keeper(clip_solid)

    out = []
    total = 0.0
    pitch = None
    for e in edges:
        c = BRepAdaptor_Curve(e)
        t = c.GetType()
        L = _path_curve_len(c)
        total += L
        if t == GeomAbs_Line:
            kind, radius = "line", None
        elif t == GeomAbs_Circle:
            kind, radius = "arc", c.Circle().Radius()
        elif t == GeomAbs_BSplineCurve:
            kind, radius = _spline_or_helix(e)
            if kind == "helix":
                pitch = _helix_pitch(e)
        else:
            kind, radius = "curve", None
        pts = _trim_to_solid(_discretize_path(e), keep, inside)
        if len(pts) < 2:
            continue                 # entirely outside the solid -> skip
        out.append({"pts3d": pts, "kind": kind,
                    "radius": radius, "length": L})
    if not out:
        return None
    if clip_solid is not None:
        _recenter_to_neutral_axis(out, clip_solid)
    return {"edges3d": out, "length": total, "pitch": pitch}


def _recenter_to_neutral_axis(edges3d, clip_solid):
    """Shift the drawn path onto the part's NEUTRAL AXIS (the spine through the
    section centroid), in place.

    cadquery's sweep rides the section's WORKPLANE ORIGIN along the path, and many
    profiles are drawn with their origin at a corner, not the centroid -- so the
    recovered path runs along an EDGE of the swept body (here it coincided with the
    arch's top outline) instead of its centre. An ISO centreline must trace the
    section centroid. We cannot recompute the true centroid spine cheaply, but the
    path's offset from the centroid is constant along its PERPENDICULAR (narrow)
    directions, so translating the path on just those axes to meet the solid's
    centre-of-mass puts it on the neutral axis without disturbing its travel."""
    try:
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp
        g = GProp_GProps(); BRepGProp.VolumeProperties_s(clip_solid, g)
        com = (g.CentreOfMass().X(), g.CentreOfMass().Y(), g.CentreOfMass().Z())
    except Exception:
        return
    allpts = [p for e in edges3d for p in e["pts3d"]]
    if len(allpts) < 2:
        return
    lo = [min(p[i] for p in allpts) for i in range(3)]
    hi = [max(p[i] for p in allpts) for i in range(3)]
    spans = [hi[i] - lo[i] for i in range(3)]
    smax = max(spans) or 1.0
    means = [sum(p[i] for p in allpts) / len(allpts) for i in range(3)]
    # shift only on axes the path barely travels along (perpendicular to travel)
    shift = [0.0, 0.0, 0.0]
    for i in range(3):
        if spans[i] < 0.30 * smax:
            shift[i] = com[i] - means[i]
    if all(abs(s) < 1e-6 for s in shift):
        return
    # SAFETY GATE: only recentre if it does NOT push the spine out of the solid.
    # The section-origin offset is the common case (recentre helps), but for some
    # parts the path is already on the neutral axis and the centroid sits in a
    # cavity/asymmetric mass, so shifting to it would move the spine into empty
    # space. Compare how many points lie inside before vs after and keep the shift
    # only when it is at least as good.
    try:
        from OCP.BRepClass3d import BRepClass3d_SolidClassifier
        from OCP.TopAbs import TopAbs_OUT
        cls = BRepClass3d_SolidClassifier(clip_solid)

        def _in_frac(pts):
            n = ins = 0
            for (x, y, z) in pts:
                cls.Perform(gp_Pnt(x, y, z), 1e-6)
                n += 1
                if cls.State() != TopAbs_OUT:
                    ins += 1
            return ins / n if n else 0.0
        before = _in_frac(allpts)
        shifted = [(x + shift[0], y + shift[1], z + shift[2])
                   for (x, y, z) in allpts]
        after = _in_frac(shifted)
        if after < before - 1e-9:          # recentre would make it worse -> skip
            return
    except Exception:
        return
    for e in edges3d:
        e["pts3d"] = [(x + shift[0], y + shift[1], z + shift[2])
                      for (x, y, z) in e["pts3d"]]


def _path_curve_len(c):
    from OCP.GCPnts import GCPnts_AbscissaPoint
    try:
        return GCPnts_AbscissaPoint.Length_s(c)
    except Exception:
        return 0.0


def _spline_or_helix(edge):
    """A BSpline path is a HELIX if its discretized points wind around a fixed
    axis with a steady rise; else a generic free curve. Returns (kind, radius):
    radius = helix radius for a helix, else None."""
    pts = _discretize_path(edge, 0.5)
    if len(pts) < 8:
        return "curve", None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
    # candidate axis = the coordinate with the largest monotone travel
    rng = [max(a) - min(a) for a in (xs, ys, zs)]
    axis = rng.index(max(rng))
    other = [i for i in range(3) if i != axis]
    cu = sum(p[other[0]] for p in pts) / len(pts)
    cv = sum(p[other[1]] for p in pts) / len(pts)
    radii = [math.hypot(p[other[0]] - cu, p[other[1]] - cv) for p in pts]
    rmean = sum(radii) / len(radii)
    if rmean < 1e-6:
        return "curve", None
    # helix: near-constant radius about the axis AND the path winds through more
    # than ~3/4 of a full turn (a real helix spins around; a gentle free-form
    # spline does not). Total wrap angle is robust where per-step spacing is not.
    spread = (max(radii) - min(radii)) / rmean
    wrap = 0.0
    prev = None
    for p in pts:
        a = math.atan2(p[other[1]] - cv, p[other[0]] - cu)
        if prev is not None:
            d = a - prev
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            wrap += d
        prev = a
    if spread < 0.18 and abs(wrap) > 0.75 * 2 * math.pi:
        return "helix", rmean
    return "curve", None


def _helix_pitch(edge):
    """Axial rise per full turn, from the discretized winding."""
    pts = _discretize_path(edge, 0.5)
    if len(pts) < 8:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
    rng = [max(a) - min(a) for a in (xs, ys, zs)]
    axis = rng.index(max(rng))
    other = [i for i in range(3) if i != axis]
    cu = sum(p[other[0]] for p in pts) / len(pts)
    cv = sum(p[other[1]] for p in pts) / len(pts)
    # total wrapped angle
    ang = 0.0
    prev = None
    for p in pts:
        a = math.atan2(p[other[1]] - cv, p[other[0]] - cu)
        if prev is not None:
            d = a - prev
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            ang += d
        prev = a
    turns = abs(ang) / (2 * math.pi)
    rise = max(p[axis] for p in pts) - min(p[axis] for p in pts)
    return rise / turns if turns > 1e-6 else None


def project_to_view(pts3d, paper_x, paper_y):
    """Map posed 3D points to a view's 2D (x,y) by the same dot-product mapping
    project() uses (paper_x -> drawing X, paper_y -> drawing Y)."""
    out = []
    for (x, y, z) in pts3d:
        px = x * paper_x[0] + y * paper_x[1] + z * paper_x[2]
        py = x * paper_y[0] + y * paper_y[1] + z * paper_y[2]
        out.append((px, py))
    return out


# ===========================================================================
# SECTION VIEWS -- full section for parts with dense internal (hidden) detail
# ===========================================================================
# ISO discourages dimensioning to hidden lines; when a view's hidden/visible
# line-length ratio is high, the standard answer is a SECTION: cut the part on
# the symmetry plane through the origin (parts are normalize_pose-centred),
# remove the half toward the viewer, and show the cut view with hatched cut
# faces (ISO 128-50). project() puts the viewer on the +(paper_x x paper_y)
# side, so the removed half is { p : p . d > 0 }.

def hidden_ratio(view):
    """hidden/visible line-length ratio of a projected view dict."""
    def _ln(pls):
        t = 0.0
        for pl in pls:
            for i in range(len(pl) - 1):
                t += math.hypot(pl[i+1][0]-pl[i][0], pl[i+1][1]-pl[i][1])
        return t
    vis = _ln(view.get("visible", []))
    return (_ln(view.get("hidden", [])) / vis) if vis > 1e-6 else 0.0


# For a section in <key>, which ADJACENT view shows the cutting plane edge-on,
# which of its local axes the plane position varies along (0=x, 1=y), and the
# sign mapping that local coordinate back to the model coordinate along the
# sectioned view's direction (top local y = -y_model, hence -1.0).
_SECTION_STATION = {
    "front": ("top",   1, -1.0),
    "left":  ("front", 0, +1.0),
    "top":   ("front", 1, +1.0),
}


def section_plane_stations(shape, view_name, views, k=3):
    """Candidate cutting-plane offsets along the view direction for a full
    section in `view_name`, best first. A cut through empty symmetric material
    shows a featureless hatched wall; real drawings cut THROUGH the internal
    detail. The detail's position along the cut axis is visible in the ADJACENT
    view (where the cutting line is drawn): its HIDDEN lines mark obscured
    internal geometry and its hole-circle centres mark drilled features, both in
    local coords along the cutting-line axis. Stations are ranked by the
    length/size-weighted density of that evidence (window 5% of extent) and up
    to `k` DISTINCT ones (>= 8% of extent apart) are returned in MODEL coords,
    ready for section_cut(offset=...). The caller test-cuts each candidate and
    keeps the most revealing one."""
    adj, ai, sign = _SECTION_STATION[view_name]
    v = views.get(adj) or {}
    stations = []                                  # (local coord, weight)
    for pl in v.get("hidden", []):
        for i in range(len(pl) - 1):
            a, b = pl[i], pl[i+1]
            L = math.hypot(b[0]-a[0], b[1]-a[1])
            if L > 1e-6:
                stations.append(((a[ai] + b[ai]) / 2.0, L))
    try:
        for (r, cx, cy, _full, is_hole, _cov) in circles_for_views(shape).get(adj, []):
            if is_hole:                            # a drilled feature: cut its axis
                stations.append(((cx, cy)[ai], 4.0 * math.pi * r))
    except Exception:
        pass
    pts = [p[ai] for pl in v.get("visible", []) for p in pl]
    if not stations or not pts:
        return []
    lo, hi = min(pts), max(pts)
    span = hi - lo
    if span <= 1e-6:
        return []
    tol = 0.05 * span
    scored = []
    for (s0, _w) in stations:
        wsum = sum(w for (s1, w) in stations if abs(s1 - s0) <= tol)
        scored.append((wsum, s0))
    scored.sort(key=lambda t: (-t[0], abs(t[1])))
    pad = 0.05 * span
    picks = []
    for (_w, s0) in scored:
        s0 = max(lo + pad, min(hi - pad, s0))
        if all(abs(s0 - p) > 0.08 * span for p in picks):
            picks.append(s0)
            if len(picks) >= k:
                break
    return [sign * p for p in picks]


def section_cut(shape, view_name, offset=0.0):
    """Cut `shape` for a full section in `view_name`. Returns
    (half_solid, cut_polys) -- cut_polys: list of faces, each a list of 2D
    segments [(x0,y0,x1,y1), ...] in the view's paper coords (the cut-face
    boundary, for hatching). The cutting plane sits at `offset` along the view
    direction d (0 = through the origin; see section_plane_offset for feature-
    aware placement); the viewer-side half (p . d > offset) is removed."""
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
    px = VIEWS[view_name]["paper_x"]; py = VIEWS[view_name]["paper_y"]
    d = _cross(px, py)
    bb = Bnd_Box(); BRepBndLib.Add_s(shape, bb)
    x0, y0, z0, x1, y1, z1 = bb.Get()
    m = 2.0   # margin so the box safely covers the half
    lo = [x0 - m, y0 - m, z0 - m]; hi = [x1 + m, y1 + m, z1 + m]
    # axis-aligned view dir: clamp the box to the removed half {p.d>offset}
    for ax in range(3):
        if d[ax] > 0.5:
            lo[ax] = offset
        elif d[ax] < -0.5:
            hi[ax] = -offset
    box = BRepPrimAPI_MakeBox(gp_Pnt(lo[0], lo[1], lo[2]),
                              gp_Pnt(hi[0], hi[1], hi[2])).Shape()
    half = BRepAlgoAPI_Cut(shape, box).Shape()
    # collect CUT faces: planar faces lying ON the cutting plane (normal // d,
    # at `offset` from the origin along d)
    cut_polys = []
    exp = TopExp_Explorer(half, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        s = BRepAdaptor_Surface(face)
        if s.GetType() == GeomAbs_Plane:
            pl = s.Plane()
            n = pl.Axis().Direction()
            ndot = n.X()*d[0] + n.Y()*d[1] + n.Z()*d[2]
            if abs(ndot) > 0.999:
                # distance of plane from origin along d
                loc = pl.Location()
                dist = loc.X()*d[0] + loc.Y()*d[1] + loc.Z()*d[2]
                if abs(dist - offset) < 1e-4:
                    segs = []
                    eexp = TopExp_Explorer(face, TopAbs_EDGE)
                    while eexp.More():
                        edge = TopoDS.Edge_s(eexp.Current())
                        pts3 = _edge_points3d(edge, deflection=0.1)
                        pts2 = project_to_view(pts3, px, py)
                        for i in range(len(pts2) - 1):
                            segs.append((pts2[i][0], pts2[i][1],
                                         pts2[i+1][0], pts2[i+1][1]))
                        eexp.Next()
                    if segs:
                        cut_polys.append(segs)
        exp.Next()
    return half, cut_polys


def _edge_points3d(edge, deflection=0.1):
    """Discretize an edge to 3D points."""
    curve = BRepAdaptor_Curve(edge)
    try:
        gc = GCPnts_QuasiUniformDeflection(curve, deflection)
        if gc.IsDone() and gc.NbPoints() >= 2:
            return [(gc.Value(i).X(), gc.Value(i).Y(), gc.Value(i).Z())
                    for i in range(1, gc.NbPoints() + 1)]
    except Exception:
        pass
    p0 = curve.Value(curve.FirstParameter())
    p1 = curve.Value(curve.LastParameter())
    return [(p0.X(), p0.Y(), p0.Z()), (p1.X(), p1.Y(), p1.Z())]


def hatch_segments(face_segs, spacing=2.5, angle_deg=45.0):
    """ISO 128-50 hatching for ONE cut face given its boundary segments (2D,
    view-local). Even-odd fill with 45-deg lines: for each hatch scanline,
    intersect all boundary segments, sort the hits along the line, fill between
    alternate pairs. Returns [(x0,y0,x1,y1), ...] hatch lines (view-local)."""
    if not face_segs:
        return []
    a = math.radians(angle_deg)
    u = (math.cos(a), math.sin(a))            # along the hatch line
    v = (-u[1], u[0])                          # across (line spacing direction)
    # project boundary points on u/v to bound the scan range
    pts = [(s[0], s[1]) for s in face_segs] + [(s[2], s[3]) for s in face_segs]
    sv = [p[0]*v[0] + p[1]*v[1] for p in pts]
    su = [p[0]*u[0] + p[1]*u[1] for p in pts]
    out = []
    # tiny phase offset avoids scanlines passing exactly through vertices (the
    # classic even-odd degeneracy)
    c = min(sv) + 0.5 * spacing + 1e-3
    while c < max(sv):
        # hatch line: p = c*v + t*u, t in [min(su), max(su)]
        hits = []
        for (x0, y0, x1, y1) in face_segs:
            # segment param s in [0,1]; solve (P0 + s*(P1-P0)) . v = c
            d0 = x0*v[0] + y0*v[1]
            d1 = x1*v[0] + y1*v[1]
            if abs(d1 - d0) < 1e-12:
                continue                       # parallel to hatch line
            s = (c - d0) / (d1 - d0)
            if 0.0 <= s < 1.0:                 # half-open: no double-count at joints
                hx = x0 + s * (x1 - x0); hy = y0 + s * (y1 - y0)
                hits.append(hx*u[0] + hy*u[1])
        hits.sort()
        for i in range(0, len(hits) - 1, 2):
            t0, t1 = hits[i], hits[i+1]
            if t1 - t0 > 0.05:
                p0 = (c*v[0] + t0*u[0], c*v[1] + t0*u[1])
                p1 = (c*v[0] + t1*u[0], c*v[1] + t1*u[1])
                out.append((p0[0], p0[1], p1[0], p1[1]))
        c += spacing
    return out


# --------------------------------------------------------------------------- #
# ISO 128 centre lines: axes of holes, bosses and shafts
# --------------------------------------------------------------------------- #
def hole_axes(shape, min_cov_turns=0.6, min_radius=0.3):
    """Axes of the part's holes, bosses and shafts for ISO 128-24 centre lines.

    Circular edges and cylindrical faces are grouped by their 3D axis (direction up
    to sign, axis position within 0.3 mm). The angular coverage of a group is the
    union over its entities, measured in the plane normal to the axis, so a fillet
    band (a quarter turn) is rejected while a hole mouth broken out at a corner
    (> 0.6 turn) or a full boss is kept -- the same rule circles_for_views applies.
    Returns [{"r": largest radius, "p": (x, y, z) axis point, "d": unit direction,
              "t0", "t1": extent of the group along d (model units)}].
    """
    NBIN = 72
    cands = []
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge_s(exp.Current())
        c = BRepAdaptor_Curve(edge)
        if c.GetType() == GeomAbs_Circle:
            circ = c.Circle()
            ax = circ.Axis().Direction(); loc = circ.Location()
            cands.append((circ.Radius(), (ax.X(), ax.Y(), ax.Z()),
                          (loc.X(), loc.Y(), loc.Z()),
                          _edge_points3d(edge, deflection=0.05)))
        exp.Next()
    fexp = TopExp_Explorer(shape, TopAbs_FACE)
    while fexp.More():
        face = TopoDS.Face_s(fexp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            cyl = surf.Cylinder()
            ax = cyl.Axis().Direction(); loc = cyl.Location()
            pts = []
            eexp = TopExp_Explorer(face, TopAbs_EDGE)
            while eexp.More():
                pts += _edge_points3d(TopoDS.Edge_s(eexp.Current()), deflection=0.05)
                eexp.Next()
            if pts:
                cands.append((cyl.Radius(), (ax.X(), ax.Y(), ax.Z()),
                              (loc.X(), loc.Y(), loc.Z()), pts))
        fexp.Next()

    def _unit(v):
        n = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) or 1.0
        return (v[0] / n, v[1] / n, v[2] / n)

    def _dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    groups = []   # dicts: d, p, e1, e2, rs, bins, t0, t1
    for (r, a, ctr, pts) in cands:
        if r < min_radius or not pts:
            continue
        d = _unit(a)
        # canonical sign: first non-negligible component positive
        for k in range(3):
            if abs(d[k]) > 1e-6:
                if d[k] < 0:
                    d = (-d[0], -d[1], -d[2])
                break
        t_c = _dot(ctr, d)
        p = (ctr[0] - t_c * d[0], ctr[1] - t_c * d[1], ctr[2] - t_c * d[2])
        g = None
        for gg in groups:
            if abs(_dot(gg["d"], d)) > 0.999 and \
               math.dist(gg["p"], p) < 0.3:
                g = gg
                break
        if g is None:
            # perpendicular basis for angular coverage
            ref = (1.0, 0.0, 0.0) if abs(d[0]) < 0.9 else (0.0, 1.0, 0.0)
            e1 = _unit(_cross(d, ref)); e2 = _cross(d, e1)
            g = {"d": d, "p": p, "e1": e1, "e2": e2, "rs": [], "bins": set(),
                 "t0": float("inf"), "t1": float("-inf")}
            groups.append(g)
        g["rs"].append(r)
        angs = []
        for q in pts:
            t = _dot(q, g["d"])
            g["t0"] = min(g["t0"], t); g["t1"] = max(g["t1"], t)
            w = (q[0] - g["p"][0] - t * g["d"][0], q[1] - g["p"][1] - t * g["d"][1],
                 q[2] - g["p"][2] - t * g["d"][2])
            if _dot(w, w) < (0.3 * r) ** 2:
                continue
            angs.append(math.atan2(_dot(w, g["e2"]), _dot(w, g["e1"])))
        for ang in angs:
            g["bins"].add(int((ang + math.pi) / (2 * math.pi) * NBIN) % NBIN)
        for a1, a2 in zip(angs, angs[1:]):
            diff = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) <= math.radians(40):
                steps = int(abs(diff) / (2 * math.pi) * NBIN) + 1
                for k in range(1, steps):
                    am = a1 + diff * k / steps
                    g["bins"].add(int((am + math.pi) / (2 * math.pi) * NBIN) % NBIN)
    out = []
    for g in groups:
        cov = len(g["bins"]) / NBIN
        if cov < min_cov_turns or g["t1"] - g["t0"] < 1e-6:
            continue
        out.append({"r": max(g["rs"]), "p": g["p"], "d": g["d"],
                    "t0": g["t0"], "t1": g["t1"], "cov": round(cov, 3)})
    return out


def centre_marks_for_views(shape):
    """hole_axes -> per-view centre marks for drawing.render(centre_marks=...):
    {"view","kind":"cross","cx","cy","r"} where the axis is along the view
    direction (true circle), {"view","kind":"axis","x0","y0","x1","y1"} where the
    axis lies in the view plane. Coords are the view's (paper_x, paper_y) frame,
    the same frame as project() and circles_for_views()."""
    marks = []
    for hx in hole_axes(shape):
        d = hx["d"]; p = hx["p"]
        for v in ("front", "top", "left"):
            px = VIEWS[v]["paper_x"]; py = VIEWS[v]["paper_y"]
            vd = _cross(px, py)
            n = math.sqrt(vd[0] ** 2 + vd[1] ** 2 + vd[2] ** 2) or 1.0
            along = abs(d[0] * vd[0] + d[1] * vd[1] + d[2] * vd[2]) / n
            if along > 0.98:
                cx = p[0] * px[0] + p[1] * px[1] + p[2] * px[2]
                cy = p[0] * py[0] + p[1] * py[1] + p[2] * py[2]
                marks.append({"view": v, "kind": "cross", "cx": cx, "cy": cy, "r": hx["r"]})
            elif along < 0.02:
                P0 = (p[0] + hx["t0"] * d[0], p[1] + hx["t0"] * d[1], p[2] + hx["t0"] * d[2])
                P1 = (p[0] + hx["t1"] * d[0], p[1] + hx["t1"] * d[1], p[2] + hx["t1"] * d[2])
                marks.append({"view": v, "kind": "axis",
                              "x0": P0[0] * px[0] + P0[1] * px[1] + P0[2] * px[2],
                              "y0": P0[0] * py[0] + P0[1] * py[1] + P0[2] * py[2],
                              "x1": P1[0] * px[0] + P1[1] * px[1] + P1[2] * px[2],
                              "y1": P1[0] * py[0] + P1[1] * py[1] + P1[2] * py[2]})
    return marks
