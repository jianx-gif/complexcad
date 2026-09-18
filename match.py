"""
Match named build parameters to actual geometry in the projected views, so each
dimension is drawn against the edge/circle it really measures, while the TEXT
shows the nominal parameter value (per spec).

A parameter is matched only if its value equals (within tolerance) a measurable
quantity in one of its preferred views:
  - linear_h : a horizontal edge span  (paper X extent in that view)
  - linear_v : a vertical edge span     (paper Y extent)
  - depth    : a vertical edge span in TOP / horizontal in LEFT
  - diameter : a circle diameter (2*r) in that view
  - radius   : a circle radius
Unmatched params are returned separately so completeness is auditable.
"""
import math
import iso_knowledge as iso

# matching tolerance: relative + absolute floor (mm, model units). The floor is
# generous enough to absorb a chamfer/fillet clipping a nominal edge by a few mm
# (e.g. a 20 mm edge measured as 19.5 after a 0.5 chamfer each side).
_REL_TOL = 0.04
# Absolute floor for LINEAR edge matching. 1.0 mm absorbs meshing/deflection
# noise and a small chamfer leg clipping a nominal edge, yet stays below the
# 1.5 mm gap between a 2.5 step and a 4 wall so they can't be conflated. The
# real guard against a small value stealing a larger edge is "closest edge +
# edge dedup" in match_params, not the floor alone.
_ABS_TOL = 1.0


def _close(a, b):
    # Adaptive absolute floor: a small feature (e.g. a 2 mm wall) must match an
    # edge whose length is genuinely ~2 mm, so the floor shrinks for small values
    # (0.4 mm here) and only opens up to _ABS_TOL for larger edges where a
    # chamfer can legitimately clip a few mm. Prevents a 1.4 mm stray edge from
    # being read as a nominal 2.
    m = max(abs(a), abs(b))
    floor = min(_ABS_TOL, 0.2 * m)
    return abs(a - b) <= max(floor, _REL_TOL * m)


def _ekey(coords, view=""):
    """Hashable identity for a measured edge (rounded coords + view), so two
    different parameters can't both claim the very same edge."""
    return (view,) + tuple(round(c, 1) for c in coords)


# Circles carry EXACT nominal sizes (a ⌀5 hole is modelled as exactly r=2.5), so
# the generous linear floor must NOT apply — otherwise ⌀5/⌀6 and r4.5/r5 get
# conflated and a callout lands on the wrong concentric circle. Tight tolerance.
_CIRC_ABS_TOL = 0.25


def _close_circ(a, b):
    return abs(a - b) <= max(_CIRC_ABS_TOL, _REL_TOL * max(abs(a), abs(b)))


# Integer-snap tolerance (mm, model units). Tessellation noise and tiny corner
# fillets shift view bboxes by a few hundredths at the NATIVE (true-mm) scale,
# so 0.12 catches them. The KOOR pipeline runs on quantized geometry scaled up
# ~100x, where the SAME noise becomes a few WHOLE units (0.02mm -> 2 units), so
# that pipeline raises this to scale*0.12 at runtime. Native drawings keep 0.12.
_SNAP_TOL = 0.12
# Snap GRID. Native: 1 (snap to whole mm). Koor pipeline sets this to `scale`
# so a quantized dimension snaps to the nearest SCALE multiple -- i.e. back to a
# whole original-mm value (299.47 -> round(2.9947)*100 = 300), which a plain
# nearest-integer snap can't do once noise pushes it past the .5 midpoint.
_SNAP_GRID = 1.0
# When True (koor pipeline, scale<100 parts), a value that SNAPPED to the grid
# is then rounded to a whole unit for DISPLAY. A non-integer scale (89.196)
# puts the grid multiple itself off the integer (35*89.196 = 3121.86), so the
# label would still read a decimal; rounding the snapped value to 3122 keeps
# big-part drawings showing clean integers. Only snapped values are rounded --
# a genuinely non-grid measurement is left exactly as measured.
_SNAP_INT_DISPLAY = False
# Per-view internal-dimension caps. Defaults keep native drawings readable; the
# koor pipeline raises these so big parts get fuller internal dimensioning.
_WALL_MAX_NEW = 4        # extra wall-gap dims added per call (wall_dims)
_SECTION_MAX = 6         # internal dims read off a section's cut faces
_LOC_MAX = 5             # location dims per view (location_dims)


def _snap(v, tol=None, grid=None):
    """Snap a measured value to its nominal: tessellation noise shifts view
    bboxes off the value the designer meant (30.02 -> 30; quantized 299.47 ->
    300). Snaps to the nearest multiple of `grid` (default _SNAP_GRID) when
    within `tol` (default _SNAP_TOL); otherwise the measured value stands so a
    genuinely non-grid dimension (a 30deg taper's projected edge) is not forced.
    A half-grid value stays as measured (as likely real as noise)."""
    if tol is None:
        tol = _SNAP_TOL
    if grid is None:
        grid = _SNAP_GRID
    n = round(v / grid) * grid
    if abs(v - n) <= tol:
        return float(round(n)) if _SNAP_INT_DISPLAY else float(n)
    return v


def _cluster_instances(insts, gap, ext_idx=None):
    """Single-linkage cluster (cx,cy)-bearing instances: two instances join the
    same cluster when within `gap` of each other (directly or via a chain). Used
    to count CONNECTED runs of a repeated feature -- a chamfer/fillet that wraps a
    boss in one continuous ring is ONE place, not N faces; truly separate features
    (four distinct hole rims) stay N. Returns a list of clusters (lists of insts).

    ext_idx: optional tuple index of each instance's EXTENT (its reach from the
    centre, e.g. half the face bbox diagonal). When given, two instances link if
    their centre distance <= ext_i + ext_j + gap -- i.e. their faces (nearly)
    touch. This chains the long faces of one continuous ring chamfer (centres far
    apart, faces end-to-end) without conflating genuinely separate features."""
    n = len(insts)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i

    for i in range(n):
        xi, yi = insts[i][1], insts[i][2]
        for j in range(i + 1, n):
            xj, yj = insts[j][1], insts[j][2]
            lim = gap
            if ext_idx is not None:
                lim = gap + insts[i][ext_idx] + insts[j][ext_idx]
            if (xi - xj) ** 2 + (yi - yj) ** 2 <= lim * lim:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(insts[i])
    return list(groups.values())


def _merge_runs(pl):
    """Collapse runs of consecutive COLLINEAR segments of a polyline into single
    segments. Two segments are collinear if their unit directions agree (cross
    product ~0) AND point the same way. A tessellated straight edge collapses to
    one long segment; a genuine arc (direction turns every step) stays split into
    its short pieces, so it can't masquerade as a long straight edge.
    Returns [(x0,y0,x1,y1), ...]."""
    if len(pl) < 2:
        return []
    out = []
    sx, sy = pl[0]                      # current run start
    px, py = pl[0]                      # previous vertex
    cdx, cdy = None, None               # current run direction (unit-ish)
    for (x, y) in pl[1:]:
        dx, dy = x - px, y - py
        ln = math.hypot(dx, dy)
        if ln < 1e-9:
            continue
        ux, uy = dx / ln, dy / ln
        if cdx is None:
            cdx, cdy = ux, uy
        elif abs(cdx * uy - cdy * ux) < 0.02 and (cdx * ux + cdy * uy) > 0:
            pass                        # still collinear -> extend the run
        else:
            out.append((sx, sy, px, py))    # close previous run
            sx, sy = px, py
            cdx, cdy = ux, uy
        px, py = x, y
    out.append((sx, sy, px, py))
    return out


def _contour_lines(view):
    """Return (vx, hy): sorted lists of x-positions of VERTICAL contour edges and
    y-positions of HORIZONTAL contour edges in the view (view-local coords). A
    dimension endpoint that coincides with one of these aligns its extension line
    to a real silhouette edge; one that doesn't floats into open space."""
    vx, hy = [], []
    for pl in view["visible"]:
        for (x0, y0, x1, y1) in _merge_runs(pl):
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy)
            if ln < 0.5:
                continue
            if abs(dx) < 0.05 * ln:          # vertical edge -> a fixed x line
                vx.append((x0 + x1) / 2.0)
            elif abs(dy) < 0.05 * ln:        # horizontal edge -> a fixed y line
                hy.append((y0 + y1) / 2.0)
    return sorted(vx), sorted(hy)


def _endpoint_align_penalty(edge, kind, lines):
    """How poorly an edge's endpoints align to view contour lines (lower = better).
    For a horizontal dimension each endpoint should land on a VERTICAL contour
    line (so its extension line coincides with a silhouette edge); for a vertical
    dimension, on a HORIZONTAL line. Returns the summed distance from each endpoint
    to the nearest such line."""
    vx, hy = lines
    x0, y0, x1, y1 = edge
    if kind == iso.KIND_LINEAR_V:
        lo = hy                              # endpoints vary in y -> match y-lines
        pts = (y0, y1)
    else:                                    # linear_h / depth measured horizontally
        lo = vx
        pts = (x0, x1)
    if not lo:
        return 0.0
    return sum(min(abs(p - q) for q in lo) for p in pts)


def _line_pairs(view):
    """Distances between PARALLEL contour lines, as dimension candidates.
    Plate thickness, pocket/step depth, wall height... often have NO single
    clean edge of their nominal length (fillets/chamfers clip the literal edge,
    adjacent features fragment it), yet the two bounding contour LINES are
    always there, and dimensioning between two parallel lines is standard ISO
    practice. Returns (vpairs, hpairs):
      vpairs: [(gap, (xm, y1, xm, y2), n_hidden)] gaps between HORIZONTAL lines
              (for linear_v / depth-in-top)
      hpairs: [(gap, (x1, ym, x2, ym), n_hidden)] gaps between VERTICAL lines
              (for linear_h / depth-in-left)
    n_hidden counts how many of the two lines are hidden-line contours: visible
    pairs are preferred, but a blind pocket's floor line only exists hidden, so
    hidden-backed pairs are allowed as a last resort. Lines must OVERLAP by
    >= 2 mm in their run direction so the extension lines have a real anchor."""
    hl, vl = [], []                       # (coord, lo, hi, hidden)
    for src, hid in (("visible", 0), ("hidden", 1)):
        for pl in view.get(src, []):
            for (x0, y0, x1, y1) in _merge_runs(pl):
                ln = math.hypot(x1 - x0, y1 - y0)
                if ln < 1.0:
                    continue
                if abs(y1 - y0) < 0.05 * ln:
                    hl.append(((y0 + y1) / 2.0, min(x0, x1), max(x0, x1), hid))
                elif abs(x1 - x0) < 0.05 * ln:
                    vl.append(((x0 + x1) / 2.0, min(y0, y1), max(y0, y1), hid))
    # merge near-identical lines (same coord within 0.1, overlapping extents)
    def _merge(lines):
        lines.sort()
        out = []
        for (c, lo, hi, hid) in lines:
            m = next((o for o in out if abs(o[0] - c) < 0.1
                      and lo <= o[2] + 0.5 and hi >= o[1] - 0.5), None)
            if m is None:
                out.append([c, lo, hi, hid])
            else:
                m[1] = min(m[1], lo); m[2] = max(m[2], hi)
                m[3] = min(m[3], hid)          # visible wins for the pair count
        # bound the O(n^2) pairing: keep the longest 60 lines
        out.sort(key=lambda l: l[1] - l[2])
        return out[:60]
    hl = _merge(hl); vl = _merge(vl)

    def _pairs(lines, vertical_gap):
        res = []
        for i in range(len(lines)):
            c1, lo1, hi1, h1 = lines[i]
            for j in range(i + 1, len(lines)):
                c2, lo2, hi2, h2 = lines[j]
                gap = abs(c2 - c1)
                if gap < 0.8:
                    continue
                lo, hi = max(lo1, lo2), min(hi1, hi2)
                if hi - lo < 2.0:
                    continue                   # no shared anchor span
                mid = (lo + hi) / 2.0
                if vertical_gap:               # horizontal lines -> vertical dim
                    edge = (mid, min(c1, c2), mid, max(c1, c2))
                else:
                    edge = (min(c1, c2), mid, max(c1, c2), mid)
                res.append((gap, edge, h1 + h2))
        return res
    return _pairs(hl, True), _pairs(vl, False)


def _edge_spans(view):
    """Axis-aligned edge spans WITH endpoints (view-local model coords), so a
    matched dimension can be drawn on the actual edge it measures, not the whole
    view. Returns (hor, ver) where each item is (length, (x0,y0,x1,y1)).
    Adds the overall bbox span as a synthetic edge so nominal overall sizes
    still match (and dimension correctly) when chamfers clip the literal edge."""
    hor, ver = [], []
    xs, ys = [], []
    for pl in view["visible"]:
        for (x, y) in pl:
            xs.append(x); ys.append(y)
        # Merge CONSECUTIVE COLLINEAR segments first. Tessellation splits one
        # straight edge into many short segments (e.g. a 23 mm side becomes 14
        # pieces ~2 mm each); without merging, a 2 mm wall_thickness would wrongly
        # match one of those pieces. Merging restores the true edge length.
        for (x0, y0, x1, y1) in _merge_runs(pl):
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy)
            if ln < 1e-6:
                continue
            if abs(dy) < 0.05 * ln:      # ~horizontal
                hor.append((ln, (x0, y0, x1, y1)))
            elif abs(dx) < 0.05 * ln:    # ~vertical
                ver.append((ln, (x0, y0, x1, y1)))
    if xs:                               # overall bbox spans (full extent)
        xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
        hor.append((xmax - xmin, (xmin, ymin, xmax, ymin)))
        ver.append((ymax - ymin, (xmin, ymin, xmin, ymax)))
    return hor, ver


def _chamfer_edges(view, circles=None):
    """Diagonal edges that look like a chamfer slant. Returns
    [(legs, (x0,y0,x1,y1), (mx,my)), ...] where `legs` is the SET of candidate
    chamfer-size values this slant could measure and (mx,my) is the edge midpoint
    for the leader anchor.

    A SYMMETRIC (45-deg) chamfer projects with dx == dy, so its size is that
    common leg. An ASYMMETRIC chamfer (e.g. cq .chamfer(0.5, 0.2887)) projects
    with dx != dy; by convention its nominal distance equals the LARGER projected
    leg, so we also offer max(dx,dy) (and the mean, for the symmetric case). The
    caller matches the nominal value against ANY of these, so both chamfer styles
    resolve while the guards below still keep arcs/noise out.

    Operates on MERGED runs so a real chamfer stays ONE straight slant, whereas a
    tessellated circle/arc collapses to many tiny non-collinear pieces that are
    rejected (a circle's segments each look ~45-deg and used to be mistaken for a
    chamfer). Also explicitly drops any slant whose midpoint lies on a known
    circle, so a hole outline can never be read as a chamfer."""
    circles = circles or []
    out = []
    for pl in view["visible"]:
        runs = _merge_runs(pl)
        for (x0, y0, x1, y1) in runs:
            dx, dy = abs(x1 - x0), abs(y1 - y0)
            ln = math.hypot(dx, dy)
            # Require a GENUINE slant: both projected legs non-trivial relative to
            # the segment. This still rejects near-horizontal / near-vertical
            # edges (which are linear dims, not chamfers). We no longer demand
            # ~45 deg, so asymmetric chamfers pass, but the 0.2*ln floor on BOTH
            # legs keeps it from grabbing a shallow stray edge.
            if ln < 1e-6 or dx < 0.2 * ln or dy < 0.2 * ln:
                continue
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            # reject if the slant lies on a circle's circumference (arc segment)
            on_circle = any(abs(math.hypot(mx - cr[1], my - cr[2]) - cr[0]) < 0.4 * cr[0]
                            for cr in circles)
            if on_circle:
                continue
            # Candidate sizes this slant could measure: the symmetric leg
            # (mean), the asymmetric larger/smaller leg, AND the slant's own
            # projected LENGTH `ln`. A 45-deg chamfer whose bevel edge faces the
            # view projects its true face width as `ln` (== chamfer distance),
            # while its dx/dy legs are only ln/sqrt(2); offering ln lets such a
            # chamfer resolve instead of being dropped as too-small.
            legs = {round((dx + dy) / 2.0, 4), round(max(dx, dy), 4),
                    round(min(dx, dy), 4), round(ln, 4)}
            out.append((legs, (x0, y0, x1, y1), (mx, my)))
    return out


def _angle_corners(view, circles=None):
    """Real, VISIBLE angles in a view: two straight edges meeting at a shared
    vertex. Returns [(deg, (vx,vy), (ux1,uy1), (ux2,uy2)), ...] = the angle, its
    vertex, and the two outward unit directions (for drawing the arc).

    Only genuine measurable angles are reported, so an angle dimension never
    lands on tessellation noise: edges must be reasonably long, neither edge may
    lie on a circle (arc pieces), and trivial ~90 deg corners are dropped (a
    right angle is implied by the views, never dimensioned)."""
    circles = circles or []
    runs = []
    for pl in view["visible"]:
        for r in _merge_runs(pl):
            if math.hypot(r[2] - r[0], r[3] - r[1]) >= 5.0:   # long edges only
                runs.append(r)

    def _on_circle(mx, my):
        return any(abs(math.hypot(mx - cr[1], my - cr[2]) - cr[0]) < 0.4 * cr[0]
                   for cr in circles)

    out = []
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            a, b = runs[i], runs[j]
            pa = [(a[0], a[1]), (a[2], a[3])]
            pb = [(b[0], b[1]), (b[2], b[3])]
            sh = next(((x) for x in pa for y in pb
                       if math.hypot(x[0] - y[0], x[1] - y[1]) < 0.6), None)
            if sh is None:
                continue
            oa = pa[0] if pa[1] == sh else pa[1]
            ob = pb[0] if pb[1] == sh else pb[1]
            v1 = (oa[0] - sh[0], oa[1] - sh[1]); v2 = (ob[0] - sh[0], ob[1] - sh[1])
            n1 = math.hypot(*v1); n2 = math.hypot(*v2)
            if n1 < 5 or n2 < 5:
                continue
            if _on_circle(*sh):
                continue
            ang = math.degrees(math.acos(
                max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))))
            if abs(ang - 90.0) < 4.0 or ang < 6.0 or ang > 174.0:
                continue                       # skip right angles / degenerate
            out.append((ang, sh, (v1[0] / n1, v1[1] / n1),
                        (v2[0] / n2, v2[1] / n2)))
    return out


def _circles(view):
    """Circle radii present in a view (from the projected circle metadata)."""
    return view.get("circles", [])


def _view_bbox(view):
    xs, ys = [], []
    for pl in view["visible"]:
        for (x, y) in pl:
            xs.append(x); ys.append(y)
    if not xs:
        return 0, 0, 0, 0
    return min(xs), min(ys), max(xs), max(ys)


def overall_dims(views_model, params):
    """Always produce the part's three OVERALL dimensions — FRONT width &
    height, TOP depth — using the view bbox spans (robust even when slots/ribs
    break the literal corner edge). The TEXT uses the nearest matching nominal
    parameter value when one is within tolerance, else the measured span.
    Returns a list of dicts {orient, view, span(x0,y0,x1,y1 view-local), text}."""
    vals = [v for v in params.values() if v > 0]

    def label(measure):
        near = [v for v in vals if _close(v, measure)]
        v = min(near, key=lambda v: abs(v - measure)) if near else measure
        # koor big parts: no nominal param matched the measured span (it is a
        # composite extent), so snap the measure to the scale grid and show it
        # as a whole unit -- otherwise the overall reads a decimal (9990, ok,
        # but 3121.86 etc. need the grid+int-display path).
        if not near:
            v = _snap(measure)
        return (str(int(round(v))) if abs(v - round(v)) < 1e-6
                else f"{v:.1f}")

    out = []
    if "front" in views_model:
        x0, y0, x1, y1 = _view_bbox(views_model["front"])
        out.append({"orient": "h", "view": "front", "value": x1 - x0,
                    "span": (x0, y0, x1, y0), "text": label(x1 - x0)})
        out.append({"orient": "v", "view": "front", "value": y1 - y0,
                    "span": (x1, y0, x1, y1), "text": label(y1 - y0)})
    if "top" in views_model:
        x0, y0, x1, y1 = _view_bbox(views_model["top"])
        out.append({"orient": "v", "view": "top", "value": y1 - y0,
                    "span": (x1, y0, x1, y1), "text": label(y1 - y0)})
    return out


def _position_candidates(circles):
    """Distances that a spacing/offset/pitch parameter could equal: pairwise
    centre distances (full + per-axis) and each centre's offset from the view
    origin (for 'offset from centre' style params). circles=[(r,cx,cy),...]."""
    cs = [(c[1], c[2]) for c in circles]
    out = []
    for i in range(len(cs)):
        cx, cy = cs[i]
        out.append(abs(cx)); out.append(abs(cy))             # offset from axis/centre
        for j in range(i + 1, len(cs)):
            dx = abs(cs[j][0] - cx); dy = abs(cs[j][1] - cy)
            out += [dx, dy, math.hypot(dx, dy)]
    return [v for v in out if v > 1e-6]


def _spacing_edge(circles, value):
    """For a POSITION/pitch dimension of magnitude `value`, find two circle
    centres in the view separated by `value` along a SINGLE axis, and return the
    centre-to-centre edge (x0,y0,x1,y1) so it draws as a real spacing dimension.
    Prefers the CLOSEST such pair (adjacent holes, the true pitch) and an
    axis-aligned separation (the other axis nearly equal), so the dimension line
    is horizontal or vertical like a normal pitch callout. None if no pair fits."""
    cs = [(c[1], c[2]) for c in circles]
    best = None
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            ax, ay = cs[i]; bx, by = cs[j]
            dx = abs(bx - ax); dy = abs(by - ay)
            # X-pitch: same row (dy ~ 0), dx == value
            if dy < 0.2 * max(dx, 1e-6) and _close(value, dx):
                if best is None or dx < best[0]:
                    best = (dx, (ax, ay, bx, by))
            # Y-pitch: same column (dx ~ 0), dy == value
            elif dx < 0.2 * max(dy, 1e-6) and _close(value, dy):
                if best is None or dy < best[0]:
                    best = (dy, (ax, ay, bx, by))
    return best[1] if best else None


def match_params(params, views_model, circles_by_view, fillets_by_view=None,
                 chamfers_by_view=None, bevels_by_view=None, rects_by_view=None):
    """params: {name: value}; views_model: {view: projection dict};
    circles_by_view: {view: [(r,cx,cy,is_full,is_hole), ...]};
    fillets_by_view: {view: [(r,cx,cy), ...]} radii of fillet/round SURFACES
        (cylinders/tori) -- a fallback target for RADIUS params whose round has
        no projectable circular edge (a top-edge round on a swept body).
    chamfers_by_view: {view: [(size,cx,cy), ...]} sizes of CHAMFER cone faces --
        a fallback target for CHAMFER params whose bevel is on a circular edge
        (a disc/bore rim) and so projects no flat 45-deg slant of the true size.
    Returns (matched, unmatched). matched is a list of dicts:
      {name, value, kind, symbol, view, measure, text}."""
    matched, unmatched = [], []
    spans = {v: _edge_spans(views_model[v]) for v in views_model}
    # Per view, the x-positions of VERTICAL contour edges and y-positions of
    # HORIZONTAL ones. A linear dimension reads cleanest when each of its
    # endpoints sits ON such a contour line (its extension line then runs along a
    # real silhouette edge, not floating into an inner corner). Used to break ties
    # among equal-length candidate edges toward the well-aligned one.
    contour = {v: _contour_lines(views_model[v]) for v in views_model}
    # Engineering-convention selection: don't repeat the same (kind, value) in
    # multiple views; remember what's already dimensioned.
    seen = set()
    claimed_edges = set()       # (view-tagged) edge coords already taken
    pair_cache = {}             # view -> _line_pairs result, built on demand
    # Search order: a parameter's preferred views first, then any remaining view.
    all_views = [v for v in ("front", "top", "left") if v in views_model]
    for name, value in params.items():
        c = iso.classify_param(name)
        if not c:
            unmatched.append((name, value, "not-a-dimension"))
            continue
        kind, sym, prefer = c
        # A radius-named param routed to DIAMETER (outer_radius, flange_radius...)
        # holds a RADIUS value but must be dimensioned as a diameter, so double it
        # so it matches the geometry's diameter and prints the right Ø value.
        if kind == iso.KIND_DIAMETER and name.lower().rsplit("_", 1)[-1] in (
                "radius", "rad", "r"):
            value = value * 2.0
        order = [v for v in prefer if v in views_model]
        order += [v for v in all_views if v not in order]   # then the rest
        hit = None
        circle_ctr = None
        edge = None              # (x0,y0,x1,y1) view-local coords of measured edge
        angle_geom = None        # (vertex, dir1, dir2) for an angle dimension
        arc_partial = False      # matched circle is a small broken-out arc -> R
        # LINEAR kinds: choose the GLOBAL best edge across ALL views, not the
        # first view with any length-coincident edge. View preference order is
        # only the FINAL tiebreak; match quality (length error bucket, then how
        # well the endpoints align to real contour lines) comes first -- so a
        # slot's own well-anchored edge in TOP beats a same-length outline
        # fragment that happens to come first in FRONT.
        if kind in (iso.KIND_LINEAR_H, iso.KIND_LINEAR_V, iso.KIND_DEPTH):
            best = None                      # (key, view, edge)
            for oi, view in enumerate(order):
                hor, ver = spans[view]
                if kind == iso.KIND_LINEAR_H:
                    cand = hor
                elif kind == iso.KIND_LINEAR_V:
                    cand = ver
                else:  # depth = Y extent: never in FRONT (see comment below)
                    if view == "front":
                        continue
                    cand = ver if view == "top" else hor
                near = [ec for ec in cand if _close(value, ec[0])
                        and _ekey(ec[1], view) not in claimed_edges]
                # DEPTH validity: the edge must SPAN toward a depth face, not
                # hug a single boundary line mid-view (see original rationale).
                if kind == iso.KIND_DEPTH and near:
                    bx0, by0, bx1, by1 = _view_bbox(views_model[view])
                    if view == "left":
                        lo, hi = bx0, bx1
                        pos = lambda ec: (ec[1][0], ec[1][2])
                    else:  # top
                        lo, hi = by0, by1
                        pos = lambda ec: (ec[1][1], ec[1][3])
                    tol = 0.10 * (hi - lo)

                    def _reaches_face(ec):
                        a, b = pos(ec)
                        return (min(abs(a - lo), abs(b - lo)) <= tol
                                or min(abs(a - hi), abs(b - hi)) <= tol)
                    near = [ec for ec in near if _reaches_face(ec)]
                lines = contour[view]
                for ec in near:
                    k = (round(abs(ec[0] - value) * 2) / 2.0,   # 0.5 mm bucket
                         _endpoint_align_penalty(ec[1], kind, lines),
                         abs(ec[0] - value), oi)
                    if best is None or k < best[0]:
                        best = (k, view, ec[1])
            # LINE-PAIR fallback (also global): the value is the distance
            # between two PARALLEL contour lines. Visible pairs first, hidden
            # last; closer value, then view preference.
            if best is None:
                for oi, view in enumerate(order):
                    if kind == iso.KIND_DEPTH and view == "front":
                        continue
                    if view not in pair_cache:
                        pair_cache[view] = _line_pairs(views_model[view])
                    vp, hp = pair_cache[view]
                    if kind == iso.KIND_LINEAR_V:
                        pcand = vp
                    elif kind == iso.KIND_LINEAR_H:
                        pcand = hp
                    else:                  # depth: top -> vert, left -> hor
                        pcand = vp if view == "top" else hp
                    for pc in pcand:
                        if not _close(value, pc[0]) \
                                or _ekey(pc[1], view) in claimed_edges:
                            continue
                        k = (pc[2], abs(pc[0] - value), oi)
                        if best is None or k < best[0]:
                            best = (k, view, pc[1])
            if best is not None:
                hit, edge = best[1], best[2]
                claimed_edges.add(_ekey(edge, hit))
        for view in (() if hit is not None or kind in (
                iso.KIND_LINEAR_H, iso.KIND_LINEAR_V, iso.KIND_DEPTH)
                else order):
            hor, ver = spans[view]
            if kind in (iso.KIND_DIAMETER, iso.KIND_RADIUS):
                circ = circles_by_view.get(view, [])
                # The PARAMETER NAME already settled hole-vs-fillet (classify_param
                # -> diameter for *_hole/*_dia/bore, radius for *_fillet/*_round),
                # so trust it and match by radius, preferring the geometrically
                # consistent circle but FALLING BACK to any arc of the right size:
                #  - DIAMETER: prefer a hole-classified circle (full or large arc);
                #    fall back to ANY circle -- a hole drilled into a sloped/swept
                #    face projects only a small (e.g. 90-deg) mouth arc, which must
                #    still receive its Ø rather than be dropped.
                #  - RADIUS: prefer a non-hole arc (a real fillet); fall back to any
                #    circle so an unusual fillet projection still gets its R.
                want_hole = (kind == iso.KIND_DIAMETER)
                fac = 2 if want_hole else 1
                prefer = [(fac * r, cx, cy, is_full, is_hole, cov)
                          for (r, cx, cy, is_full, is_hole, cov) in circ
                          if is_hole == want_hole]
                anyc = [(fac * r, cx, cy, is_full, is_hole, cov)
                        for (r, cx, cy, is_full, is_hole, cov) in circ]
                near = [t for t in prefer if _close_circ(value, t[0])]
                if not near:                       # fall back to any same-size arc
                    near = [t for t in anyc if _close_circ(value, t[0])]
                # RADIUS-only last resort: match a fillet/round SURFACE (cylinder
                # /torus) of this radius. A round whose edge does not project as an
                # axis-aligned circle (top-edge round on a swept body) has no entry
                # in `circ`, but its blend surface carries the true radius, so this
                # recovers an otherwise-undimensioned R.
                if not near and kind == iso.KIND_RADIUS and fillets_by_view:
                    near = [(r, cx, cy, False, False, 1.0) for (r, cx, cy, _e)
                            in fillets_by_view.get(view, [])
                            if _close_circ(value, r)]
                m_hit = min(near, key=lambda t: abs(t[0] - value)) if near else None
                if m_hit:
                    hit = view; circle_ctr = (m_hit[1], m_hit[2])
                    # a SMALL leftover arc (a hole broken out at the part corner
                    # keeps only a quarter notch): per ISO 129-1 an arc well
                    # under a half circle is dimensioned as R, not Ø. A boss
                    # whose wall is half-exposed (cov ~0.5 turn) keeps its Ø.
                    arc_partial = m_hit[5] <= 0.35
                    break
            elif kind == iso.KIND_CHAMFER:
                # a chamfer shows as a slant; its nominal SIZE equals one of the
                # candidate legs the slant projects (symmetric -> equal X/Y leg,
                # asymmetric -> the larger leg). An EDGE chamfer sits on the
                # part's outer corner, so among the size-matching slants prefer
                # the one closest to a view-bbox corner -> avoids grabbing an
                # internal feature's slant (e.g. a pin-root outline that happens
                # to project a 1 mm leg).
                def _leg_err(ce):
                    # smallest distance from `value` to ANY candidate leg
                    return min(abs(value - lg) for lg in ce[0])
                cand = [ce for ce in _chamfer_edges(
                            views_model[view], circles_by_view.get(view, []))
                        if any(_close(value, lg) for lg in ce[0])]
                if cand:
                    bx0, by0, bx1, by1 = _view_bbox(views_model[view])
                    corners = [(bx0, by0), (bx0, by1), (bx1, by0), (bx1, by1)]
                    diag = math.hypot(bx1 - bx0, by1 - by0)

                    def _corner_dist(ce):
                        mx, my = ce[2]
                        return min(math.hypot(mx - cx, my - cy)
                                   for (cx, cy) in corners)
                    m_hit = min(cand, key=lambda ce: (_corner_dist(ce),
                                                      _leg_err(ce)))
                    # Only accept an EDGE chamfer that actually sits on an outer
                    # corner. If the nearest 45deg slant is far from every corner
                    # it's an internal feature's outline, not the edge chamfer ->
                    # leave it unmatched rather than mislabel (no-bad-dim rule).
                    if _corner_dist(m_hit) <= 0.15 * diag:
                        hit = view; edge = m_hit[1]; circle_ctr = m_hit[2]; break
                # CHAMFER fallback: a bevel on a CIRCULAR edge (disc/bore rim) is a
                # CONE face, not a flat slant -- _chamfer_edges cannot see it and
                # the rim's projected leg is foreshortened, so the nominal size
                # never matches. The cone face carries the exact chamfer size; use
                # it so rim chamfers (a core deliverable) are never dropped.
                if chamfers_by_view:
                    cfit = [(sz, cx, cy) for (sz, cx, cy)
                            in chamfers_by_view.get(view, [])
                            if _close(value, sz)]
                    if cfit:
                        m_hit = min(cfit, key=lambda t: abs(t[0] - value))
                        hit = view; circle_ctr = (m_hit[1], m_hit[2]); break
            elif kind == iso.KIND_ANGLE:
                # match a real, visible angle between two edges (closest in deg).
                # Many design angles (cone/countersink, twist, bend in 3D) are NOT
                # visible without a section view, so most legitimately stay
                # unmatched rather than being forced onto noise.
                cand = [ac for ac in _angle_corners(
                            views_model[view], circles_by_view.get(view, []))
                        if abs(ac[0] - value) <= 3.0]
                m_hit = min(cand, key=lambda ac: abs(ac[0] - value),
                            default=None)
                if m_hit:
                    hit = view; angle_geom = (m_hit[1], m_hit[2], m_hit[3]); break
            elif kind == iso.KIND_POSITION:
                if any(_close(value, mm) for mm in _position_candidates(
                        circles_by_view.get(view, []))):
                    hit = view; break
        if hit is None:
            unmatched.append((name, value, "no-geometry-match"))
            continue
        # A diameter param whose circle survives only as a SMALL arc (hole
        # broken out at a corner/edge -> a notch) is dimensioned as a RADIUS:
        # there is no circle on the drawing for a Ø to describe, and ISO labels
        # sub-half arcs with R. The displayed value is the honest radius.
        if kind == iso.KIND_DIAMETER and arc_partial:
            kind = iso.KIND_RADIUS
            value = value / 2.0
            sym = "R"
        # Dedup only a TRUE repeat: same kind + value + view. The same value in
        # a different view (e.g. pocket_length in TOP vs block_width in LEFT) is
        # a distinct dimension and must be kept.
        key = (kind, round(value, 2), hit)
        if key in seen:
            unmatched.append((name, value, "duplicate-in-same-view"))
            continue
        seen.add(key)
        # Count IDENTICAL features for the ISO "n x <size>" shorthand: how many
        # SEPARATE holes of this diameter appear in the hit view. ISO 129-1 labels
        # a repeated hole pattern once as e.g. "8x ⌀5". Count distinct hole CENTRES
        # (cluster the matching circles): one hole drilled into a sloped/swept face
        # projects its mouth as SEVERAL concentric or near-coincident arcs, which
        # must count as ONE hole, not several -- clustering merges them so a single
        # counterbore is not mis-reported as "6x". Truly separate holes sit far
        # apart and stay distinct.
        count = 1
        if kind == iso.KIND_DIAMETER:
            hits = [(r, cx, cy) for (r, cx, cy, is_full, is_hole, _cov)
                    in circles_by_view.get(hit, [])
                    if is_hole and _close_circ(value, 2 * r)]
            if hits:
                # gap scales with the hole size: arcs of one mouth fall within a
                # few radii; separate holes are spaced much wider.
                gap = max(4.0, 1.2 * value)
                count = max(1, len(_cluster_instances(hits, gap)))
        # A POSITION (spacing/pitch) dimension measures the distance between two
        # feature centres. Find the pair of circle centres in the hit view whose
        # separation along ONE axis equals the value, and record that as the edge
        # so it draws as a real centre-to-centre dimension (not silently dropped).
        if kind == iso.KIND_POSITION and edge is None:
            edge = _spacing_edge(circles_by_view.get(hit, []), value)
        matched.append({
            "name": name, "value": value, "kind": kind, "symbol": sym,
            "view": hit, "text": iso.format_value(kind, sym, value),
            "center": circle_ctr,   # (cx,cy) for circle dims, else None
            "edge": edge,           # (x0,y0,x1,y1) measured edge for linear dims
            "angle": angle_geom,    # (vertex, dir1, dir2) for an angle dim, else None
            "count": count,         # repeated-feature count for "n x" prefix
        })

    # ---- geometry-driven fallback: label ROUND/FILLET arcs the params missed ----
    # A build parameter that names a round (corner_radius, edge_fillet...) often
    # fails to match: a later chamfer/fillet RESHAPES the feature, so the surviving
    # surface radius (e.g. 5.66) no longer equals the nominal value (8). The arc is
    # still plainly VISIBLE in the view, so leaving it bare reads as a missed
    # dimension. Here every fillet/round SURFACE detected in a view that is NOT
    # already covered by a matched circle callout at that spot gets an R from its
    # MEASURED radius -- the honest, in-the-solid value. This is the catch-all that
    # stops visible corner rounds / edge fillets from going unlabelled regardless of
    # whether a parameter happens to name them.
    _fillet_fallback(matched, fillets_by_view, circles_by_view)
    # ---- geometry-driven fallback: label CHAMFER bevels the params missed ----
    # The parameter matcher only accepts an edge chamfer on an OUTER corner, so a
    # chamfer on an INTERNAL feature (a boss/pocket/rib rim, a slot mouth) -- a
    # core deliverable -- is left bare. Every flat slanted bevel detected in a view
    # that no matched chamfer already covers gets a C from its measured leg.
    _chamfer_fallback(matched, bevels_by_view)
    # ---- geometry-driven fallback: size RECTANGULAR pockets/bosses ----
    # A pocket/boss/recess has a width x depth that no outline parameter names and
    # the matcher misses (its depth axis isn't the Z its name implies), so the
    # rectangle reads undimensioned. Stamp its footprint W x D in TOP.
    _rect_fallback(matched, rects_by_view, views_model)
    # ---- GUARANTEE (thesis core): script chamfer/fillet => drawn C/R --------
    # A .chamfer()/.fillet() call in the build script ALWAYS leaves bevel/cone/
    # blend geometry in the part, so when a parameter names one, at least one
    # C (R) callout must appear. If matching AND the fallbacks above all came
    # up empty (a veto misfired, an exotic projection), label the detected
    # geometry whose measured size is closest to the named value -- honest,
    # in-the-solid, and never silently dropped.
    def _kinds_wanted(kind):
        vals = []
        for n, v in params.items():
            c2 = iso.classify_param(n)
            if c2 and c2[0] == kind:
                vals.append(v * (2.0 if kind == iso.KIND_DIAMETER else 1.0))
        return vals
    want_c = _kinds_wanted(iso.KIND_CHAMFER)
    if want_c and not any(m["kind"] == iso.KIND_CHAMFER for m in matched):
        pool = []
        for view, lst in (chamfers_by_view or {}).items():
            pool += [(sz, cx, cy, view) for (sz, cx, cy) in lst]
        for view, lst in (bevels_by_view or {}).items():
            pool += [(sz, cx, cy, view) for (sz, cx, cy, _e) in lst]
        if pool:
            sz, cx, cy, view = min(
                pool, key=lambda t: min(abs(t[0] - w) for w in want_c))
            sz = round(sz, 2)
            matched.append({
                "name": "_chamfer_g", "value": sz, "kind": iso.KIND_CHAMFER,
                "symbol": "", "view": view,
                "text": iso.format_value(iso.KIND_CHAMFER, "", sz),
                "center": (cx, cy), "edge": None, "angle": None, "count": 1,
            })
    want_r = _kinds_wanted(iso.KIND_RADIUS)
    if want_r and not any(m["kind"] == iso.KIND_RADIUS for m in matched):
        pool = []
        for view, lst in (fillets_by_view or {}).items():
            pool += [(r, cx, cy, view) for (r, cx, cy, _e) in lst]
        if pool:
            r, cx, cy, view = min(
                pool, key=lambda t: min(abs(t[0] - w) for w in want_r))
            r = round(r, 2)
            matched.append({
                "name": "_fillet_g", "value": r, "kind": iso.KIND_RADIUS,
                "symbol": "R", "view": view,
                "text": iso.format_value(iso.KIND_RADIUS, "R", r),
                "center": (cx, cy), "edge": None, "angle": None, "count": 1,
            })
    return matched, unmatched


def _rect_fallback(matched, rects_by_view, views_model):
    """Append W and D linear dims for rectangular pocket/boss footprints that no
    matched edge already dimensions."""
    if not rects_by_view:
        return
    # A rectangular feature already explicitly dimensioned by a parameter that
    # matched an edge AT THIS FEATURE is covered. We only suppress a rect dim when
    # a matched edge of that length sits ON this rectangle's boundary (same
    # location) -- NOT merely shares the numeric value with an unrelated dim
    # elsewhere (a pocket's 15 mm depth must still be shown even if a 15 mm pitch
    # is dimensioned across the part).
    edge_dims = []      # (view, value, midx, midy, horizontal)
    for m in matched:
        e = m.get("edge")
        if e and m.get("kind") in (iso.KIND_LINEAR_H, iso.KIND_LINEAR_V,
                                   iso.KIND_DEPTH, iso.KIND_POSITION):
            edge_dims.append((m["view"], m.get("value"),
                              (e[0] + e[2]) / 2.0, (e[1] + e[3]) / 2.0,
                              abs(e[3] - e[1]) <= abs(e[2] - e[0])))

    def _already(view, val, horiz, bb):
        """A matched linear dim of this value & orientation whose measured edge
        lies WITHIN this rectangle (+2 mm) already dimensions the feature --
        whether it sits on the boundary or across the middle (a line-pair match
        between the pocket walls runs through the centre)."""
        x0, y0, x1, y1 = bb
        return any(v == view and val is not None and _close(val, vv)
                   and hz == horiz
                   and x0 - 2.0 <= ex <= x1 + 2.0 and y0 - 2.0 <= ey <= y1 + 2.0
                   for (v, vv, ex, ey, hz) in edge_dims)

    for view, rects in rects_by_view.items():
        # group identical-size rectangles: a repeated pocket/boss pattern (four
        # 4.5x4.5 pads) is ONE size labelled once, not N callouts. Bucket by
        # (w,h) to 0.1 mm; emit on one representative per size.
        groups = {}
        for (w, h, cx, cy) in rects:
            groups.setdefault((round(w * 10), round(h * 10)), []).append((w, h, cx, cy))
        for key, inst in groups.items():
            w = sum(t[0] for t in inst) / len(inst)
            h = sum(t[1] for t in inst) / len(inst)
            rep = inst[len(inst) // 2]
            cx, cy = rep[2], rep[3]
            hw, hh = w / 2.0, h / 2.0
            cnt = len(inst)
            bb = (cx - hw, cy - hh, cx + hw, cy + hh)
            # WIDTH (horizontal) edge along the bottom of the rectangle
            if not _already(view, w, True, bb):
                matched.append({
                    "name": "_rect_w", "value": _snap(round(w, 2)),
                    "kind": iso.KIND_LINEAR_H, "symbol": "",
                    "view": view, "text": iso.format_value(iso.KIND_LINEAR_H, "", _snap(round(w, 2))),
                    "center": None,
                    "edge": (cx - hw, cy - hh, cx + hw, cy - hh),
                    "angle": None, "count": cnt,
                })
            # DEPTH (vertical) edge along the right of the rectangle
            if not _already(view, h, False, bb):
                matched.append({
                    "name": "_rect_h", "value": _snap(round(h, 2)),
                    "kind": iso.KIND_LINEAR_V, "symbol": "",
                    "view": view, "text": iso.format_value(iso.KIND_LINEAR_V, "", _snap(round(h, 2))),
                    "center": None,
                    "edge": (cx + hw, cy - hh, cx + hw, cy + hh),
                    "angle": None, "count": cnt,
                })


def _chamfer_fallback(matched, bevels_by_view):
    """Append C callouts for chamfer bevels no matched dimension covers.

    A chamfer of a given size is labelled ONCE: if a parameter already named a
    chamfer of that size (in any view) the param callout stands for it; otherwise
    we add a single fallback C in the view where that size has the MOST instances
    (reads cleanest). This avoids the same C2 appearing in front+top+left for one
    feature, while still surfacing an internal chamfer the param matcher skipped."""
    if not bevels_by_view:
        return
    # already-labelled chamfer centres, per view (param match / rim cone). A
    # bevel near one of these is the SAME feature already drawn -> skip it. A
    # bevel FAR from every covered centre is a DISTINCT feature (an internal
    # boss/pocket rim vs the outer rim) and must be labelled even if it happens to
    # share the rim's size.
    covered = {}
    for m in matched:
        if m.get("kind") == iso.KIND_CHAMFER and m.get("center") is not None:
            covered.setdefault(m["view"], []).append(m["center"])
    # collect, per size bucket, the candidate (view, instances) groups, dropping
    # instances that sit on an already-labelled chamfer of that size.
    by_size = {}          # bucket -> list of (view, [instances])
    for view, bevels in bevels_by_view.items():
        cov = covered.get(view, [])
        groups = {}
        for (sz, cx, cy, ext) in bevels:
            if any((cx - ux) ** 2 + (cy - uy) ** 2 < 9.0 for (ux, uy) in cov):
                continue                           # same spot as a drawn chamfer
            groups.setdefault(round(sz * 10), []).append((sz, cx, cy, ext))
        for key, inst in groups.items():
            by_size.setdefault(key, []).append((view, inst))
    for key, cands in by_size.items():
        s0 = sum(t[0] for (_v, inst) in cands for t in inst) / \
            sum(len(inst) for (_v, inst) in cands)
        # emit ONE callout for this distinct chamfer, in the view with the most
        # instances (reads cleanest).
        view, inst = max(cands, key=lambda vi: len(vi[1]))
        # count PLACES, not faces: cluster bevels whose faces (nearly) TOUCH --
        # centre distance within ext_i+ext_j+gap -- so one continuous ring chamfer
        # (faces chained end to end around an outline, centres far apart) is ONE
        # place, while separate chamfered features stay distinct.
        clusters = _cluster_instances(inst, max(2.0, s0), ext_idx=3)
        nplaces = len(clusters)
        big = max(clusters, key=len)               # leader on the largest run
        rep = big[len(big) // 2]
        matched.append({
            "name": "_chamfer", "value": round(s0, 2),
            "kind": iso.KIND_CHAMFER, "symbol": "",
            "view": view, "text": iso.format_value(iso.KIND_CHAMFER, "", round(s0, 2)),
            "center": (rep[1], rep[2]), "edge": None, "angle": None,
            "count": nplaces,
        })


def _fillet_fallback(matched, fillets_by_view, circles_by_view):
    """Append R callouts for round/fillet surfaces no matched dimension covers."""
    if not fillets_by_view:
        return
    # circle centres already dimensioned (by name match), per view, to avoid a
    # double callout on the same arc.
    covered = {}
    matched_dias = {}        # view -> set of matched diameter VALUES
    matched_radii = {}       # view -> set of matched RADIUS values (param callouts)
    for m in matched:
        if m.get("center") is not None:
            covered.setdefault(m["view"], []).append((m["center"], m["value"],
                                                       m["kind"]))
        if m.get("kind") == iso.KIND_DIAMETER:
            matched_dias.setdefault(m["view"], set()).add(round(m["value"], 1))
        if m.get("kind") == iso.KIND_RADIUS:
            matched_radii.setdefault(m["view"], set()).add(round(m["value"], 1))
    for view, rounds in fillets_by_view.items():
        # A genuine HOLE wall is also a small cylinder, but it is already a Ø
        # target: it carries a hole circle that a matched DIAMETER dimension sits
        # on (built in `covered` below). A corner round / edge fillet matched no
        # parameter, so nothing covers it -- that's exactly what we want to label.
        # So the only veto needed is "a matched dim already describes this arc",
        # handled by `covered`; we do NOT blanket-veto by is_hole, because a corner
        # round that chamfering turned into a full circle is is_hole=True yet still
        # needs its R.
        # Hole circles in this view whose diameter is ALREADY dimensioned (matched
        # as a Ø, possibly via a "2x" repeated-feature count that names only one
        # centre). Any round concentric with one of these is that hole's wall /
        # counterbore step in a SECOND instance of the pattern -- already covered by
        # the Ø callout, so it must not also get an R.
        dias = matched_dias.get(view, set())
        vcirc = circles_by_view.get(view, [])
        hole_ctrs = [(cx, cy) for (rr, cx, cy, is_full, is_hole, _cov) in vcirc
                     if is_hole and round(2 * rr, 1) in dias]
        # A round that is the INNER step of a stepped/counterbored hole (a smaller
        # bore concentric beneath a wider, already-dimensioned mouth) is part of
        # that hole, not a fillet. Veto a round if a LARGER hole circle is
        # concentric with it -> it is a bore step, covered by the mouth's Ø.
        bore_steps = [(cx, cy, rr) for (rr, cx, cy, is_full, is_hole, _cov) in vcirc
                      if is_hole]
        # Collect the rounds that survive the hole/dup vetoes, then GROUP by radius
        # so a fillet repeated on many edges (8 plate corners, a hole-pattern ring)
        # gets ONE representative callout -- ISO 129-1 labels equal repeated rounds
        # once (optionally "n x R"), never one leader per instance (which produced
        # 20x R1 clutter on a chamfered grid plate).
        survivors = []                            # (r, cx, cy, ext)
        for (r, cx, cy, fext) in rounds:
            # Concentricity tolerance is generous (1.3 mm): a hole drilled into a
            # SLOPED or chamfered face projects its bore and counterbore mouths at
            # slightly offset centres, yet they are the same hole.
            if any(abs(hx - cx) < 1.3 and abs(hy - cy) < 1.3
                   for (hx, hy) in hole_ctrs):
                continue                          # wall of a dimensioned hole
            if any(abs(bx - cx) < 1.3 and abs(by - cy) < 1.3 and br > r + 0.1
                   for (bx, by, br) in bore_steps):
                continue                          # inner step of a stepped hole
            # skip if a matched circle dim already sits on this arc.
            #  - matched DIAMETER at this centre -> it is a HOLE/bore; its wall and
            #    any counterbore step are concentric small cylinders that must NOT
            #    get an R (the through-hole r=4.5 under a Ø12 cbore is the bore
            #    wall, not a fillet). Veto ANY round concentric with a hole.
            #  - matched RADIUS of this size at this centre -> already labelled.
            dup = False
            for (ctr, val, kind) in covered.get(view, []):
                if abs(ctr[0] - cx) < 0.6 and abs(ctr[1] - cy) < 0.6:
                    if kind == iso.KIND_DIAMETER:
                        dup = True; break          # concentric with a hole -> skip
                    if kind == iso.KIND_RADIUS and _close_circ(val, r):
                        dup = True; break
                # SAME-CYLINDER veto: this 'round' is a FRAGMENT of a cylinder
                # whose Ø is already dimensioned (a boss wall split by a slot).
                # The fillet detector centres on the fragment's surface COM,
                # the Ø callout on the AXIS -- up to one radius apart -- so the
                # concentricity test above misses it. Equal radius + centre
                # within that radius (+ slack) = the same cylinder.
                if kind == iso.KIND_DIAMETER and _close_circ(val, 2 * r) \
                        and math.hypot(ctr[0] - cx, ctr[1] - cy) <= r + 2.0:
                    dup = True; break
            if dup:
                continue
            survivors.append((r, cx, cy, fext))

        # group survivors by radius (0.1 mm bucket); one callout per distinct R
        groups = {}
        for (r, cx, cy, fext) in survivors:
            key = round(r * 10)                    # 0.1 mm bucket
            groups.setdefault(key, []).append((r, cx, cy, fext))
        # representative leader: the instance nearest a view corner reads cleanest
        bx0 = by0 = bx1 = by1 = None
        for (r, cx, cy, fext) in survivors:
            bx0 = cx if bx0 is None else min(bx0, cx)
            bx1 = cx if bx1 is None else max(bx1, cx)
            by0 = cy if by0 is None else min(by0, cy)
            by1 = cy if by1 is None else max(by1, cy)
        mradii = matched_radii.get(view, set())
        for key, inst in groups.items():
            r0 = sum(t[0] for t in inst) / len(inst)
            # a PARAMETER already labelled an R of this value in this view -> that
            # callout represents the whole repeated round family. Don't add a
            # second (double-counting) fallback R; instead promote the existing
            # callout's repeat count to the geometry count so it reads "n x R".
            pre = next((m for m in matched
                        if m["view"] == view and m["kind"] == iso.KIND_RADIUS
                        and m["name"] != "_fillet" and _close_circ(m["value"], r0)),
                       None)
            # count PLACES, not faces: cluster blends whose faces (nearly) touch
            # (centre dist <= ext_i+ext_j+gap) -- a fillet wrapping one boss/pocket
            # in a continuous ring is ONE place; separate corner rounds stay N.
            clusters = _cluster_instances(inst, max(2.0, r0), ext_idx=3)
            nplaces = len(clusters)
            if pre is not None:
                pre["count"] = max(pre.get("count", 1) or 1, nplaces)
                continue
            if bx0 is not None:
                corners = [(bx0, by0), (bx0, by1), (bx1, by0), (bx1, by1)]
                rep = min(inst, key=lambda t: min(
                    (t[1] - px) ** 2 + (t[2] - py) ** 2 for (px, py) in corners))
            else:
                rep = inst[0]
            matched.append({
                "name": "_fillet", "value": round(r0, 2),
                "kind": iso.KIND_RADIUS, "symbol": iso.SYM_RADIUS,
                "view": view, "text": iso.format_value(
                    iso.KIND_RADIUS, iso.SYM_RADIUS, round(r0, 2)),
                "center": (rep[1], rep[2]), "edge": None, "angle": None,
                "count": nplaces,                 # "n x R" for separate rounds
            })


# model axis a linear dimension measures, by (view, edge orientation)
_DIM_AXIS = {
    ("front", "h"): "x", ("front", "v"): "z",
    ("top", "h"): "x", ("top", "v"): "y",
    ("left", "h"): "y", ("left", "v"): "z",
}


def _dim_axis(m):
    e = m.get("edge")
    if e is None:
        return None
    horiz = abs(e[3] - e[1]) <= abs(e[2] - e[0])
    return _DIM_AXIS.get((m["view"], "h" if horiz else "v"))


def _view_bbox_local(view_model):
    """(xmin, ymin, xmax, ymax) of a view's drawn geometry, or None."""
    xs = [p[0] for pl in view_model.get("visible", []) for p in pl]
    ys = [p[1] for pl in view_model.get("visible", []) for p in pl]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def arc_angle_dims(matched, arcs_by_view, views_model=None, max_per_view=1):
    """Append ANGULAR dimensions (张角 / swept angle, ISO 129-1) for arc-swept /
    revolved / sector parts, from projlib.arc_angles_for_views.

    Each detected arc carries its CENTRE (the angle vertex), the two RADIUS
    directions to its endpoints (the angle's two sides) and the swept angle in
    degrees -- exactly the KIND_ANGLE payload drawing.py renders via
    annotate.angle_dim(vertex, d1, d2, text). We emit ONE angular dim per
    distinct (view, centre, sweep) so a part with one arc gets one张角, and:

      - skip an arc whose sweep DUPLICATES an angle already matched from a
        parameter (within 2 deg in the same view) -- the named angle stands;
      - cap to `max_per_view` so a multi-arc body (concentric swept bands) does
        not stack redundant equal angles;
      - the arc reads true-size only in the view projlib offered it (axis along
        the view dir), so the value is the real swept angle, not foreshortened.

    A swept angle is only meaningful where the arc shows as a true arc, so this
    NEVER fires on a plain prismatic part (a box-with-holes has no GeomAbs_Circle
    arc edge that is not a full circle) -- preventing phantom angle callouts.

    VERTEX PLACEMENT (ISO 129-1 / CAD-standard angular dim): the angle's apex IS
    the arc CENTRE and stays at its TRUE position. A shallow large-radius arc (a
    banana sweep, r=47 spanning 83 deg) has its centre far outside the drawn
    geometry, but that is fine and CORRECT: annotate.angle_dim draws EXTENSION
    LINES from the feature edge (at the real arc radius) radially out to a
    dimension arc, exactly the long converging lines CAD draws toward a distant
    vertex (see the user's reference). So we DO NOT relocate the apex anymore --
    we pass the feature RADIUS so the dimension arc is placed just outside the
    real arc edge, and let drawing.py cap the arc radius to keep it in-frame.
    views_model is kept for the (rare) sanity clamp only."""
    if not arcs_by_view:
        return matched
    out = list(matched)
    # angles already named by a parameter, per view (avoid double-labelling)
    named = {}
    for m in matched:
        if m.get("kind") == iso.KIND_ANGLE and m.get("angle") is not None:
            named.setdefault(m["view"], []).append(m["value"])
    for view, arcs in arcs_by_view.items():
        # Collapse arcs of (nearly) the SAME swept angle into one callout. The
        # inner/outer/top/bottom edges of one swept band, plus its chamfered /
        # shelled rim, project as several arcs whose sweep differs by only a few
        # degrees (e.g. 83.0 and 80.2 on the same band). Clustering by sweep
        # (within SWEEP_MERGE deg) keeps ONE张角 per distinct arc feature, with
        # the LARGEST-radius / largest-sweep representative (longest arc -> the
        # angle dimension has room to draw clear).
        SWEEP_MERGE = 6.0
        ordered = sorted(arcs, key=lambda a: (-a["sweep_deg"], -a["radius"]))
        clusters = []                             # [representative arc]
        for a in ordered:
            if any(abs(a["sweep_deg"] - c["sweep_deg"]) <= SWEEP_MERGE
                   for c in clusters):
                continue                          # same sweep as a kept arc
            if any(abs(a["sweep_deg"] - nv) <= 2.0 for nv in named.get(view, [])):
                continue                          # already a named angle here
            clusters.append(a)
        cands = clusters
        # Rank by ARC LENGTH (radius x sweep): the part's defining swept band is
        # the longest visible arc, so it wins over a smaller-radius rim cut that
        # happens to span more degrees. (Pure largest-sweep would pick an R6
        # scallop's 172 deg over a flange's 106 deg main arc.)
        cands.sort(key=lambda a: a["radius"] * a["sweep_deg"], reverse=True)
        bb = _view_bbox_local(views_model[view]) if (views_model
                                                     and view in views_model) else None
        for a in cands[:max_per_view]:
            sweep = a["sweep_deg"]
            text = iso.format_value(iso.KIND_ANGLE, iso.SYM_DEGREE, sweep)
            vx, vy = a["cx"], a["cy"]            # TRUE arc centre = angle apex
            d1, d2 = a["d1"], a["d2"]
            feat_r = float(a.get("radius", 0.0))  # feature arc radius (model mm)
            out.append({
                "name": "_arc_angle", "value": sweep,
                "kind": iso.KIND_ANGLE, "symbol": iso.SYM_DEGREE,
                "view": view, "text": text,
                "center": None, "edge": None,
                # KIND_ANGLE payload drawing.py reads: (vertex, dir1, dir2);
                # feat_r lets the renderer place the dim arc OUTSIDE the real arc
                # edge and draw extension lines from the edge out to it.
                "angle": ((vx, vy), d1, d2),
                "feat_r": feat_r,
                "count": 1,
            })
    return out


def wall_dims(matched, walls_by_view, views_model, overall=None, max_new=None):
    """Internal sizes read from OPPOSING WALL pairs (projlib.wall_gap_dims):
    through-slot width/length, channel and cavity gaps. Two actions:

    RELOCATE -- a parameter equal to a wall gap (same value, same MODEL axis)
    that matched a length-coincident edge in ANOTHER view is moved onto the
    pair: the wall pair is the feature's true geometry, the other edge was a
    fragment that merely shared the length. The dim then sits ON the feature in
    the view where it reads true-size.

    ADD -- a gap no parameter names at all (the small internal sizes that were
    the biggest completeness hole) is added as a `_wall` dim, smallest first,
    capped so a ribbed casting doesn't drown the view."""
    if max_new is None:
        max_new = _WALL_MAX_NEW
    if not walls_by_view:
        return matched
    LIN = (iso.KIND_LINEAR_H, iso.KIND_LINEAR_V, iso.KIND_DEPTH)
    used = set()
    for m in matched:
        if m.get("kind") in LIN:
            used.add(round(m["value"], 1))
    over_vals = set()
    for od in (overall or []):
        try:
            over_vals.add(round(float(od.get("text")), 1))
        except (TypeError, ValueError):
            pass
        over_vals.add(round(od.get("value", -1.0), 1))
    spans = {}
    for v, vm in views_model.items():
        xs = [p[0] for pl in vm.get("visible", []) for p in pl]
        ys = [p[1] for pl in vm.get("visible", []) for p in pl]
        if xs:
            spans[v] = (max(xs) - min(xs), max(ys) - min(ys))
    cands = []
    for view, pairs in walls_by_view.items():
        if view not in views_model:
            continue
        for (gap, edge, axis) in pairs:
            cands.append((gap, view, edge, axis))
    cands.sort(key=lambda c: c[0])              # smallest internal sizes first
    out = list(matched)
    added = 0
    done_pairs = set()                           # (axis, value) emitted already
    for (gap, view, edge, axis) in cands:
        horiz = abs(edge[3] - edge[1]) <= abs(edge[2] - edge[0])
        kind = iso.KIND_LINEAR_H if horiz else iso.KIND_LINEAR_V
        sp = spans.get(view)
        if sp and abs(gap - (sp[0] if horiz else sp[1])) < 1.0:
            continue                             # full-span: that's the overall
        if (axis, round(gap, 1)) in done_pairs:
            continue                             # one dim per distinct size+axis
        covered = False
        relocate = None
        for m in out:
            if m.get("kind") not in LIN or m.get("edge") is None:
                continue
            if not _close(m["value"], gap) or _dim_axis(m) != axis:
                continue
            if m["view"] == view:
                covered = True                   # this view already shows it
                break
            if m.get("name") and not m["name"].startswith("_"):
                relocate = m                     # param placed in another view
        done_pairs.add((axis, round(gap, 1)))
        if covered:
            continue
        if relocate is not None:
            relocate["view"] = view
            relocate["kind"] = kind
            relocate["edge"] = edge
            continue
        if added >= max_new or round(gap, 1) in used \
                or round(gap, 1) in over_vals:
            continue
        used.add(round(gap, 1))
        g = _snap(round(gap, 2))
        out.append({
            "name": "_wall", "value": g, "kind": kind, "symbol": "",
            "view": view, "text": iso.format_value(kind, "", g),
            "center": None, "edge": edge, "angle": None, "count": 1,
        })
        added += 1
    return out


def section_dims(view, faces, matched, overall=None, max_dims=None):
    """Linear dimensions of the INTERNAL structure a full section reveals, read
    straight off the CUT FACES. The whole point of sectioning is to dimension
    internals; parameter matching alone leaves most of them bare. Each cut face
    is a material cross-section: its bbox extents are wall thicknesses / floor
    depths / boss widths, and the GAPS between adjacent faces are the cavity
    inner widths/heights. Gap (cavity) sizes come first -- they are the sizes a
    reader needs most -- then face extents. Values already dimensioned anywhere
    on the drawing are skipped, so this only ADDS what name matching missed.
    Returns extra `matched`-style dicts (name=_section) drawn as normal ISO
    linear dimensions in the section view."""
    if max_dims is None:
        max_dims = _SECTION_MAX
    if not faces:
        return []
    used = set()
    for m in matched:
        if m.get("kind") in (iso.KIND_LINEAR_H, iso.KIND_LINEAR_V,
                             iso.KIND_DEPTH, iso.KIND_POSITION):
            used.add(round(m["value"], 1))
    # the OVERALL W/H/D dims are drawn too -- their text is the nominal (or
    # measured) span; a section dim repeating that value is pure duplication.
    for od in (overall or []):
        try:
            used.add(round(float(od.get("text")), 1))
        except (TypeError, ValueError):
            pass

    boxes = []
    for segs in faces:
        xs = [s[0] for s in segs] + [s[2] for s in segs]
        ys = [s[1] for s in segs] + [s[3] for s in segs]
        boxes.append((min(xs), min(ys), max(xs), max(ys)))

    # Representative sizes only -- a hole-pattern cut produces DOZENS of webs and
    # gaps; stacking each one buried the view under near-equal numbers and ran
    # the stack off the sheet. Per orientation keep just TWO sizes a reader
    # actually needs: the LARGEST cavity gap (the main internal opening) and the
    # SMALLEST wall/web thickness (the critical material section). <= 4 total.
    gaps_h, gaps_v = [], []     # (value, edge)
    # cavity widths: horizontal gaps between x-adjacent faces with y-overlap
    bx = sorted(boxes)
    for i in range(len(bx)):
        for j in range(i + 1, len(bx)):
            a, b = bx[i], bx[j]
            gap = b[0] - a[2]
            if gap <= 0.8:
                continue
            ylo, yhi = max(a[1], b[1]), min(a[3], b[3])
            if yhi - ylo < 0.3 * min(a[3] - a[1], b[3] - b[1]):
                continue
            ym = (ylo + yhi) / 2.0
            gaps_h.append((gap, (a[2], ym, b[0], ym)))
            break                       # nearest x-neighbour only
    # cavity heights: vertical gaps between y-adjacent faces with x-overlap
    by = sorted(boxes, key=lambda b: (b[1], b[0]))
    for i in range(len(by)):
        for j in range(i + 1, len(by)):
            a, b = by[i], by[j]
            gap = b[1] - a[3]
            if gap <= 0.8:
                continue
            xlo, xhi = max(a[0], b[0]), min(a[2], b[2])
            if xhi - xlo < 0.3 * min(a[2] - a[0], b[2] - b[0]):
                continue
            xm = (xlo + xhi) / 2.0
            gaps_v.append((gap, (xm, a[3], xm, b[1])))
            break
    walls_h, walls_v = [], []   # (value, edge)
    for (x0, y0, x1, y1) in boxes:
        w, h = x1 - x0, y1 - y0
        if w >= 0.8:
            walls_h.append((w, (x0, y0, x1, y0)))
        if h >= 0.8:
            walls_v.append((h, (x0, y0, x0, y1)))

    cand = []                   # (value, kind, edge) in emit order
    if gaps_h:
        cand.append(max(gaps_h) + (iso.KIND_LINEAR_H,))
    if gaps_v:
        cand.append(max(gaps_v) + (iso.KIND_LINEAR_V,))
    if walls_h:
        cand.append(min(walls_h) + (iso.KIND_LINEAR_H,))
    if walls_v:
        cand.append(min(walls_v) + (iso.KIND_LINEAR_V,))

    out = []
    for (v, edge, kind) in cand:
        if round(v, 1) in used:
            continue
        used.add(round(v, 1))
        out.append({
            "name": "_section", "value": round(v, 1), "kind": kind,
            "symbol": "", "view": view,
            "text": iso.format_value(kind, "", round(v, 1)),
            "center": None, "edge": edge, "angle": None, "count": 1,
        })
        if len(out) >= max_dims:
            break
    return out


def location_dims(view, view_model, circles, rects, matched, max_dims=None):
    """LOCATION dimensions (ISO 129-1: every feature needs SIZE + LOCATION).
    Sizes (Ø, w x h) and pitches (spacing) are matched from parameters, but
    nothing locates the features against the part DATUM edges -- the reader
    cannot place the hole pattern or the pocket on the part. For each distinct
    hole-diameter GROUP, locate its REFERENCE instance (the bottom-left one)
    from the view's left/bottom outline; locate each rect feature's centre the
    same way. Values already dimensioned (e.g. a spacing equal to the offset)
    are skipped; output is capped to stay readable."""
    if max_dims is None:
        max_dims = _LOC_MAX
    xs = [p[0] for pl in view_model.get("visible", []) for p in pl]
    ys = [p[1] for pl in view_model.get("visible", []) for p in pl]
    if not xs:
        return []
    bx0, by0 = min(xs), min(ys)
    spanx, spany = max(xs) - bx0, max(ys) - by0
    used = set()
    for m in matched:
        if m.get("kind") in (iso.KIND_LINEAR_H, iso.KIND_LINEAR_V,
                             iso.KIND_DEPTH, iso.KIND_POSITION):
            used.add(round(m["value"], 1))

    out = []

    def _emit(vx, vy):
        """Locate point (vx,vy) from the left and bottom datum edges."""
        for (val, kind, edge, span) in (
                (vx - bx0, iso.KIND_LINEAR_H, (bx0, vy, vx, vy), spanx),
                (vy - by0, iso.KIND_LINEAR_V, (vx, by0, vx, vy), spany)):
            # skip degenerate (feature ON the datum edge) and full-span values
            # (those just repeat the view's OVERALL dimension).
            if val < 1.0 or abs(val - span) < 0.8 \
                    or round(val, 1) in used or len(out) >= max_dims:
                continue
            used.add(round(val, 1))
            out.append({
                "name": "_loc", "value": _snap(round(val, 2)), "kind": kind,
                "symbol": "", "view": view,
                "text": iso.format_value(kind, "", _snap(round(val, 2))),
                "center": None, "edge": edge, "angle": None, "count": 1,
            })

    # one reference instance per distinct hole diameter (bottom-left instance)
    bygroup = {}
    for (r, cx, cy, _full, is_hole, _cov) in circles or []:
        if is_hole:
            bygroup.setdefault(round(r, 1), []).append((cx, cy))
    # ALSO locate features whose Ø was matched from a non-hole-classified arc
    # (a half-exposed boss): the matched circle centre is the AXIS, so the
    # location comes out at the nominal designed offset, not a surface-COM blur.
    circle_ctrs = []
    for m in matched:
        if m.get("kind") == iso.KIND_DIAMETER and m.get("center") \
                and m.get("view") == view:
            circle_ctrs.append(m["center"])
            bygroup.setdefault(round(m["value"] / 2.0, 1),
                               []).append(m["center"])
    for rkey in sorted(bygroup):
        ref = min(bygroup[rkey], key=lambda c: (c[1], c[0]))   # bottom-left
        _emit(ref[0], ref[1])
    # rect features (pocket/boss footprints): locate the centre. A rect that
    # CONTAINS a located circle centre is that feature's own top/floor fragment
    # (a boss top clipped by a slot) -- the circle already locates it; locating
    # the fragment's centre-of-area would stamp a meaningless decimal.
    for (w, h, cx, cy) in rects or []:
        if any(cx - w / 2 - 1 <= qx <= cx + w / 2 + 1
               and cy - h / 2 - 1 <= qy <= cy + h / 2 + 1
               for (qx, qy) in circle_ctrs):
            continue
        _emit(cx, cy)
    return out
