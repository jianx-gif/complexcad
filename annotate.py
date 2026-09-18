"""
ISO 129-1 dimension annotation primitives.

Given a view's paper-space box (x0, y0, w, h) and a side, produce the geometry
for one linear dimension: extension lines, dimension line, two arrowheads, and
the text anchor. Pure geometry (mm on paper); the caller draws it.

Only LINEAR overall dimensions in the prototype:
  - 'bottom' : horizontal dimension placed below the view (width)
  - 'right'  : vertical dimension placed right of the view (height/depth)
"""
import math
from iso_knowledge import ISO129 as K


def _arrow(px, py, dirx, diry):
    """Return the two short barb segments of a filled arrowhead at (px,py)
    pointing along (dirx,diry). Returns list of (x0,y0,x1,y1)."""
    L, W = K["arrow_len"], K["arrow_w"]
    # base center behind the tip
    bx, by = px - dirx * L, py - diry * L
    # perpendicular
    nx, ny = -diry, dirx
    p1 = (bx + nx * W / 2, by + ny * W / 2)
    p2 = (bx - nx * W / 2, by - ny * W / 2)
    return [(px, py, p1[0], p1[1]), (px, py, p2[0], p2[1]), (p1[0], p1[1], p2[0], p2[1])]


def linear_dim(box, side, text, level=0):
    """box=(x0,y0,w,h) paper mm; side in {'bottom','right'}; level stacks
    parallel dims outward. Returns dict with line lists + text placement."""
    x0, y0, w, h = box
    gap, beyond = K["ext_gap"], K["ext_beyond"]
    off = K["dim_offset"] + level * K["dim_step"]
    ext_lines, dim_lines, arrows = [], [], []

    if side == "bottom":
        yd = y0 - off                                   # dimension line y
        # extension lines from the two bottom corners down past the dim line
        for xc in (x0, x0 + w):
            ext_lines.append((xc, y0 - gap, xc, yd - beyond))
        dim_lines.append((x0, yd, x0 + w, yd))
        arrows += _arrow(x0, yd, -1, 0)                 # left arrow points left
        arrows += _arrow(x0 + w, yd, 1, 0)              # right arrow points right
        tx, ty, rot, va, ha = x0 + w / 2, yd + K["text_gap"], 0, "bottom", "center"

    elif side == "right":
        xd = x0 + w + off                               # dimension line x
        for yc in (y0, y0 + h):
            ext_lines.append((x0 + w + gap, yc, xd + beyond, yc))
        dim_lines.append((xd, y0, xd, y0 + h))
        arrows += _arrow(xd, y0, 0, -1)
        arrows += _arrow(xd, y0 + h, 0, 1)
        tx, ty, rot, va, ha = xd + K["text_gap"], y0 + h / 2, 90, "bottom", "center"
    else:
        raise ValueError(side)

    return {
        "ext": ext_lines, "dim": dim_lines, "arrows": arrows,
        "text": (tx, ty, text, rot, va, ha),
    }


def edge_dim(x0, y0, x1, y1, orient, baseline, text):
    """Dimension an edge segment (paper mm) with the dimension line placed at an
    EXTERIOR baseline (absolute coord), so it sits outside the view and rarely
    crosses geometry. Extension lines bridge from the edge to that baseline; the
    dimension line still spans only the edge, so its length equals the value.
      orient 'h': baseline is a Y below the view; 'v': baseline is an X right of
      the view."""
    gap, beyond = K["ext_gap"], K["ext_beyond"]
    ext_lines, dim_lines, arrows = [], [], []
    # ISO 129-1 §8.3: if the span is too short to fit the text BETWEEN the two
    # arrowheads, the number is moved OUTSIDE (past one arrow) so it never
    # overlaps the arrows. Estimate text length from char count at ~text_h.
    txt_len = max(1, len(str(text))) * K["text_h"] * 0.7
    need = 2 * K["arrow_len"] + txt_len
    if orient == "h":
        xa, xb = min(x0, x1), max(x0, x1)
        yd = baseline
        edge_y = min(y0, y1)
        for xc in (xa, xb):
            ext_lines.append((xc, edge_y - gap if edge_y > yd else edge_y + gap,
                              xc, yd - beyond))
        dim_lines.append((xa, yd, xb, yd))
        arrows += _arrow(xa, yd, -1, 0) + _arrow(xb, yd, 1, 0)
        if (xb - xa) >= need:                       # text fits between arrows
            tx, ty, ha = (xa + xb) / 2, yd + K["text_gap"], "center"
        else:                                       # too small -> text just past the
            # right end (arrows point inward, so the space right of xb is clear).
            tx, ty, ha = xb + K["text_gap"], yd + K["text_gap"], "left"
        rot, va = 0, "bottom"
    else:  # 'v'
        ya, yb = min(y0, y1), max(y0, y1)
        xd = baseline
        edge_x = max(x0, x1)
        for yc in (ya, yb):
            ext_lines.append((edge_x + gap if edge_x < xd else edge_x - gap,
                              yc, xd + beyond, yc))
        dim_lines.append((xd, ya, xd, yb))
        arrows += _arrow(xd, ya, 0, -1) + _arrow(xd, yb, 0, 1)
        # ISO 129-1: vertical dim text rotated 90deg, read from the RIGHT, placed
        # just LEFT of the dimension line. Normally CENTRED on the span; if the
        # span is too short, move it OUTSIDE (above the top arrow) so it clears.
        rot = 90
        if (yb - ya) >= need:                       # fits between arrows -> centred
            tx, ty, va, ha = xd - K["text_gap"], (ya + yb) / 2, "bottom", "center"
        else:                                       # too small -> text just past the
            # top of the dim line. The arrows point INWARD, so the space above yb
            # is clear; hug it (ha="left" => text body sits just above yb) so the
            # number stays close to the line it labels and reads unambiguously.
            tx, ty, va, ha = xd - K["text_gap"], yb + K["text_gap"], "bottom", "left"
    return {"ext": ext_lines, "dim": dim_lines, "arrows": arrows,
            "text": (tx, ty, text, rot, va, ha)}


def circle_dim(cx, cy, r, text, leader_len=10.0, angle_deg=45.0,
               through_center=False, text_side=0):
    """ISO diameter/radius callout: a leader from the circle edge out to a short
    shoulder with text. cx,cy,r are paper mm. angle_deg sets the leader
    direction so several CONCENTRIC callouts (counterbore/countersink) can be
    fanned to distinct angles and not overlap. The shoulder always runs toward
    the right so text reads horizontally; text sits past the shoulder end.

    through_center: contact the arc on the FAR side (opposite angle_deg) with
    the leader running through the centre -- for a CONCAVE notch arc (a hole
    broken out at a part corner) whose material faces the view interior, where
    the default near-side contact would put the arrow in empty air."""
    import math
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    if through_center:
        sx, sy = cx - r * ux, cy - r * uy              # far-side arc contact
    else:
        sx, sy = cx + r * ux, cy + r * uy              # point on circle
    ex, ey = cx + (r + leader_len) * ux, cy + (r + leader_len) * uy  # elbow
    # shoulder points toward +X (or -X if the leader already goes left) so the
    # horizontal text always trails away from the geometry. text_side=+1/-1
    # overrides (the caller flips it when the default side would run the text
    # past the drawing frame).
    sgn = text_side if text_side else (1.0 if ux >= 0 else -1.0)
    shoulder = 5.0 * sgn
    hx, hy = ex + shoulder, ey                          # horizontal shoulder end
    leader = [(sx, sy, ex, ey), (ex, ey, hx, hy)]
    # arrow at the contact point, pointing along the leader ONTO the arc
    arrows = _arrow(sx, sy, -ux, -uy)
    ha = "left" if sgn > 0 else "right"
    tgap = 1.0 * sgn
    return {
        "ext": [], "dim": [], "leader": leader, "arrows": arrows,
        "text": (hx + tgap, hy, text, 0, "center", ha),
    }


def chamfer_dim(mx, my, dirx, diry, text, leader_len=11.0, text_side=0):
    """Chamfer callout (e.g. 'C2'): a leader with an arrow touching the chamfer
    slant at its midpoint (mx,my) and running OUTWARD along (dirx,diry) to a
    short horizontal shoulder + text. dir should point away from the part.
    text_side=+1/-1 overrides the shoulder/text side (frame-overflow guard)."""
    import math
    n = math.hypot(dirx, diry) or 1.0
    ux, uy = dirx / n, diry / n
    ex, ey = mx + leader_len * ux, my + leader_len * uy   # elbow
    sgn = text_side if text_side else (1.0 if ux >= 0 else -1.0)
    hx, hy = ex + 5.0 * sgn, ey                            # horizontal shoulder
    leader = [(mx, my, ex, ey), (ex, ey, hx, hy)]
    arrows = _arrow(mx, my, -ux, -uy)                      # arrow points onto slant
    ha = "left" if sgn > 0 else "right"
    return {
        "ext": [], "dim": [], "leader": leader, "arrows": arrows,
        "text": (hx + 1.0 * sgn, hy, text, 0, "center", ha),
    }


def angle_dim(vx, vy, d1, d2, text, feat_r=0.0, dim_r=None, max_r=None,
              text_pos=None):
    """Angular dimension per ISO 129-1 / standard CAD (AutoCAD/SolidWorks) — the
    construction the user's reference image shows, with the arc CENTRE marked:

      - VERTEX (vx,vy) = the angle's apex = the arc CENTRE. A small CENTRE-LINE
        CROSS is drawn here so the reader sees which point the angle turns about.
      - the feature's real arc edge sits at radius `feat_r` from the centre.
      - EXTENSION LINES run radially along d1,d2 from just OUTSIDE the feature
        surface (feat_r + a 1..2 mm gap) all the way IN to the centre cross AND
        OUT past the dimension arc -- so both lines visibly CONVERGE at the
        centre, confirming the measurement point.
      - the DIMENSION LINE is an ARC concentric with the feature (same centre),
        radius `dim_r` placed just OUTSIDE the feature edge, spanning the SMALLER
        angle between d1 and d2 -- which is SYMMETRIC about the bisector by
        construction (both d1,d2 are radii of the same arc).
      - an ARROWHEAD at EACH arc end, tangent to the arc, terminating ON its
        extension line.
      - the VALUE is returned separately so the caller can collision-test and
        place it in clear space (default: just outside the arc, on the bisector).

    feat_r   : distance from centre to the feature arc edge (mm, paper).
    dim_r    : dim-arc radius (mm). Default feat_r + standard offset (outside it).
    max_r    : cap on dim_r so the arc stays in frame.
    text_pos : (tx,ty) to force the value position (after the caller's collision
               check); None -> default bisector placement.

    Returns dict(cross, ext, dim, arrows, text, mid_dir, dim_r, vertex) so the
    caller can both render and reason about the geometry (text bbox, etc.)."""
    import math
    a1 = math.atan2(d1[1], d1[0])
    a2 = math.atan2(d2[1], d2[0])
    # smaller signed sweep from a1 to a2 (the dimensioned quadrant, < 180°).
    # SYMMETRY: the arc is drawn a1 -> a1+da, centred on the vertex, so it is
    # automatically symmetric about the bisector mid = a1 + da/2 -- both ends are
    # equidistant from the centre (= dim_r) and from the bisector.
    da = a2 - a1
    while da <= -math.pi:
        da += 2 * math.pi
    while da > math.pi:
        da -= 2 * math.pi

    feat_r = max(0.0, float(feat_r))
    # The dimension arc must sit JUST OUTSIDE the feature arc and HUG it (concentric,
    # small offset) so the two arrowheads land right at the feature's two ends and
    # the angle reads symmetric -- a large offset would fling the arc far past the
    # arc ends and look lopsided. Use a small fixed clearance (arrowhead + a little),
    # not the full linear dim_offset (10 mm).
    ARC_OFFSET = max(4.0, K["arrow_len"] + 1.5)   # ~5 mm: clears the edge, hugs it
    MIN_DIM_R = 8.0                          # arc never collapses onto the apex
    if dim_r is None:
        dim_r = feat_r + ARC_OFFSET
    dim_r = max(dim_r, MIN_DIM_R, feat_r + 0.5 * ARC_OFFSET)
    if max_r is not None and max_r > MIN_DIM_R:
        dim_r = min(dim_r, max_r)

    surf_gap = max(1.0, min(2.0, K["ext_gap"]))   # 1..2 mm gap off the surface
    beyond = K["ext_beyond"]                       # ext line passes the arc a bit
    # EXTENSION LINES: full radial line from (feature surface + gap) IN to the
    # centre and OUT past the dim arc, so both lines converge on the centre cross.
    ext_in = 0.0                                   # reach the centre (cross)
    ext_out = dim_r + beyond
    # the small blank gap sits just outside the surface; if there is no feature
    # edge (feat_r ~ 0) start from the centre.
    seg_lo = ext_in
    ext = []
    for (dx, dy) in (d1, d2):
        # inner part: centre -> just below the surface gap (skip the 1..2mm band
        # right at the surface so the line doesn't touch the part outline)
        if feat_r > surf_gap + 0.5:
            ext.append((vx + dx * seg_lo, vy + dy * seg_lo,
                        vx + dx * (feat_r - surf_gap), vy + dy * (feat_r - surf_gap)))
            ext.append((vx + dx * (feat_r + surf_gap), vy + dy * (feat_r + surf_gap),
                        vx + dx * ext_out, vy + dy * ext_out))
        else:
            ext.append((vx + dx * seg_lo, vy + dy * seg_lo,
                        vx + dx * ext_out, vy + dy * ext_out))

    # CENTRE-LINE CROSS at the vertex (two short dash-style segments).
    cl = max(2.5, min(5.0, dim_r * 0.18))
    cross = [(vx - cl, vy, vx + cl, vy), (vx, vy - cl, vx, vy + cl)]

    # DIMENSION ARC at dim_r, spanning the smaller sweep (concentric, symmetric).
    n = max(8, int(abs(da) / 0.12))
    arc = []
    for k in range(n):
        t0 = a1 + da * k / n
        t1 = a1 + da * (k + 1) / n
        arc.append((vx + dim_r * math.cos(t0), vy + dim_r * math.sin(t0),
                    vx + dim_r * math.cos(t1), vy + dim_r * math.sin(t1)))
    # ARROWHEADS tangent to the arc at EACH end, terminating on the extension line.
    s = 1.0 if da >= 0 else -1.0
    e1 = (vx + dim_r * math.cos(a1), vy + dim_r * math.sin(a1))
    e2 = (vx + dim_r * math.cos(a2), vy + dim_r * math.sin(a2))
    t_at1 = (-math.sin(a1) * s, math.cos(a1) * s)        # tangent dir at end 1
    t_at2 = (math.sin(a2) * s, -math.cos(a2) * s)        # tangent dir at end 2
    arrows = _arrow(e1[0], e1[1], t_at1[0], t_at1[1]) + \
        _arrow(e2[0], e2[1], t_at2[0], t_at2[1])

    # VALUE: default just outside the arc on the bisector; caller may override.
    mid = a1 + da / 2.0
    mid_dir = (math.cos(mid), math.sin(mid))
    if text_pos is not None:
        tx, ty = text_pos
    else:
        tr = dim_r + K["text_gap"] + 1.5
        tx, ty = vx + tr * mid_dir[0], vy + tr * mid_dir[1]
    return {"cross": cross, "ext": ext, "dim": arc, "arrows": arrows,
            "text": (tx, ty, text, 0, "center", "center"),
            "mid_dir": mid_dir, "dim_r": dim_r, "vertex": (vx, vy)}
