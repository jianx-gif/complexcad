"""
ISO 129-1 dimensioning knowledge base.

Encodes the rules that constrain HOW a dimension is drawn so annotations stay
standard-compliant. Two parts:
  1. ISO 129-1 drawing constants/rules (extension lines, dimension lines,
     arrowheads, text placement).
  2. Parameter-name heuristics: classify a build parameter (from the py/json)
     into a dimension KIND (linear-horizontal / linear-vertical / diameter /
     radius / angle / chamfer) and the view(s) it should appear in.

This module holds NO geometry; drawing/extraction code consults it.
"""
import re

# ---------------------------------------------------------------------------
# 1) ISO 129-1 drawing rules (mm on paper, applied at paper scale)
# ---------------------------------------------------------------------------
ISO129 = {
    # Extension (witness) lines: ISO 129-1 §6.3
    "ext_gap": 1.0,        # gap between feature outline and start of ext line
    "ext_beyond": 2.0,     # ext line extends ~2 mm beyond the dimension line
    # Dimension lines: §6.2 — offset from outline, spacing between parallels
    "dim_offset": 10.0,    # first dimension line offset from the part outline
    "dim_step": 9.0,       # spacing between stacked parallel dimension lines
    # Arrowheads: §6.4 — closed filled, length:width ~ 3:1
    "arrow_len": 3.5,
    "arrow_w": 1.2,
    # Text: §8 — height, gap above dimension line, placed mid-span, readable
    "text_h": 2.5,         # nominal char height (ISO 3098); >=2.5 mm
    "text_gap": 1.0,       # gap between text and dimension line
    # Line weights (ISO 128): dimension/ext lines are thin
    "lw_thin": 0.25,
}

# Symbols — ISO 129-1 / ISO 81714
SYM_DIAMETER = "⌀"      # ⌀
SYM_RADIUS = "R"
SYM_DEGREE = "°"        # °
SYM_SQUARE = "□"        # □ (for square sections)


# ---------------------------------------------------------------------------
# 2) Parameter-name heuristics -> dimension kind + target view
# ---------------------------------------------------------------------------
# Each rule: (regex on the lowercased param name) -> dict(kind, prefer_views,
# symbol). 'kind' drives how the dimension line is drawn; 'prefer_views' is the
# ordered list of views where this dimension is most naturally placed.
#
# Model axes after normalize_pose: X = width (FRONT/TOP horizontal),
# Y = depth (TOP vertical, LEFT horizontal), Z = height (FRONT/LEFT vertical).

KIND_LINEAR_H = "linear_h"   # horizontal extent (along X)
KIND_LINEAR_V = "linear_v"   # vertical extent (along Z)
KIND_DEPTH = "depth"         # depth extent (along Y)
KIND_DIAMETER = "diameter"
KIND_RADIUS = "radius"
KIND_ANGLE = "angle"
KIND_CHAMFER = "chamfer"
KIND_POSITION = "position"   # spacing/offset/pitch between features (a distance)

# ---------------------------------------------------------------------------
# ANGULAR DIMENSION OF ARCS / SECTORS / BODIES OF REVOLUTION — ISO 129-1
# ---------------------------------------------------------------------------
# RULE (knowledge): a part built with a ROTATION / ARC SWEEP (radiusArc, revolve,
# an arc-swept profile, a circular sector) must carry the SWEPT ANGLE (张角) of
# its arc — an ANGULAR DIMENSION per ISO 129-1: value in DEGREES, symbol ° (an
# arc spanning the two bounding radii, an arrowhead at each end, the value
# outside the arc). It is placed in the view that shows the arc as a TRUE arc
# (the arc plane facing the viewer / the arc axis along the view direction); in
# a foreshortened view the angle would read wrong, so it is NOT dimensioned there.
#
# The swept angle is detected from GEOMETRY (projlib.arc_angles_for_views): a
# GeomAbs_Circle edge that is NOT a full turn, sweep = (LastParameter -
# FirstParameter) in degrees, filtered to a meaningful span (≈10°–350°, radius
# not tiny) so full circles (holes/bosses → diameter) and fillet/chamfer
# micro-arcs are excluded and never produce a phantom angle on a plain prismatic
# part. match.arc_angle_dims turns each into a KIND_ANGLE callout.
ARC_SWEEP_MIN_DEG = 10.0     # below this = a fillet/round micro-arc, not a sweep
ARC_SWEEP_MAX_DEG = 350.0    # above this ≈ a full circle (a hole), not a sector

_RULES = [
    (r"(diameter|_dia\b|\bdia\b|\bdia_|bore)", KIND_DIAMETER, SYM_DIAMETER),
    (r"(radius|_rad\b|\brad\b|fillet|_r\b)",   KIND_RADIUS,   SYM_RADIUS),
    # arc/sweep/sector angle parameters are ANGULAR dimensions too (in addition
    # to the geometry-detected swept angle): arc_angle, sweep_angle, sector_angle.
    (r"(angle|_deg|degree|taper|sweep|sector|arc_)", KIND_ANGLE, SYM_DEGREE),
    (r"(chamfer|bevel)",                        KIND_CHAMFER,  ""),
    (r"(width|_w\b|\bwidth\b|length|_len|span|outer|od\b)", KIND_LINEAR_H, ""),
    (r"(height|_h\b|\bhigh\b|thick|thk|tall|depth_z)",      KIND_LINEAR_V, ""),
    (r"(depth|_d\b|\bdepth\b|deep)",            KIND_DEPTH,    ""),
    (r"(spacing|pitch|offset|distance|gap|center|centre)",  KIND_LINEAR_H, ""),
]

# Which views each kind is preferentially dimensioned in (first that fits wins).
PREFER_VIEWS = {
    KIND_LINEAR_H: ["front", "top"],
    KIND_LINEAR_V: ["front", "left"],
    KIND_DEPTH:    ["top", "left"],
    KIND_DIAMETER: ["top", "front"],
    KIND_RADIUS:   ["front", "top"],
    # ANGLE: param-named angles prefer front/left; a GEOMETRY-detected arc sweep
    # is emitted only into the view where the arc reads true-size (its axis along
    # the view dir — projlib.arc_angles_for_views enforces this), which for a
    # disc/arc-swept part is usually TOP.
    KIND_ANGLE:    ["front", "left", "top"],
    KIND_CHAMFER:  ["front", "left"],
    KIND_POSITION: ["top", "front"],
}


# Trailing-token map: the LAST underscore token usually names the dimension
# kind (e.g. counterbore_depth -> depth, mount_hole_diameter -> diameter).
# Checked before the loose substring rules so 'bore' doesn't hijack '_depth'.
_SUFFIX = {
    "diameter": KIND_DIAMETER, "dia": KIND_DIAMETER, "bore": KIND_DIAMETER,
    "radius": KIND_RADIUS, "rad": KIND_RADIUS, "r": KIND_RADIUS, "fillet": KIND_RADIUS,
    "angle": KIND_ANGLE, "deg": KIND_ANGLE,
    "chamfer": KIND_CHAMFER, "bevel": KIND_CHAMFER,
    "width": KIND_LINEAR_H, "w": KIND_LINEAR_H, "length": KIND_LINEAR_H,
    "len": KIND_LINEAR_H, "span": KIND_LINEAR_H,
    "height": KIND_LINEAR_V, "h": KIND_LINEAR_V, "thickness": KIND_LINEAR_V,
    "thk": KIND_LINEAR_V, "tall": KIND_LINEAR_V,
    "depth": KIND_DEPTH, "deep": KIND_DEPTH, "d": KIND_DEPTH,
    "spacing": KIND_POSITION, "pitch": KIND_POSITION, "offset": KIND_POSITION,
    "distance": KIND_POSITION, "gap": KIND_POSITION,
}
_SYM = {KIND_DIAMETER: SYM_DIAMETER, KIND_RADIUS: SYM_RADIUS,
        KIND_ANGLE: SYM_DEGREE, KIND_CHAMFER: "",
        KIND_LINEAR_H: "", KIND_LINEAR_V: "", KIND_DEPTH: "",
        KIND_POSITION: ""}


def classify_param(name):
    """Return (kind, symbol, prefer_views) for a parameter name, or None.
    The trailing token wins (counterbore_depth -> depth); fall back to loose
    substring rules for names without a clear suffix."""
    n = name.lower()
    last = n.rsplit("_", 1)[-1]
    # A trailing axis qualifier (_x/_y/_z) names a DIRECTION, not a dimension
    # kind, so drop it and use the token before it: 'hole_spacing_x' -> spacing
    # (a POSITION/pitch), not the loose 'spacing'->linear fallback. Likewise
    # 'pitch_y', 'offset_x'.
    if last in ("x", "y", "z") and "_" in n[:-2]:
        last = n[:-2].rstrip("_").rsplit("_", 1)[-1]
    # 'chamfer'/'bevel' names the FEATURE, so its SIZE is a chamfer dimension
    # regardless of the size-token suffix used (chamfer_distance / chamfer_size /
    # chamfer_len / chamfer_depth all denote the chamfer leg). Without this the
    # trailing-token rule below mis-routes 'chamfer_distance' -> position,
    # 'chamfer_depth' -> depth, etc., and the chamfer never gets a C<size>
    # callout. EXCEPTION: an explicit chamfer ANGLE (chamfer_angle[_deg]) is a
    # genuine angle dimension, not a C-size, so let the suffix handle it.
    if ("chamfer" in n or "bevel" in n) and last not in ("angle", "deg", "degree"):
        return KIND_CHAMFER, _SYM[KIND_CHAMFER], PREFER_VIEWS[KIND_CHAMFER]
    # A *_radius / *_rad token is a FILLET radius (R) ONLY when the feature is an
    # edge round; when it names a whole revolved/outline circle (outer_radius,
    # inner_radius, base/disk/flange/cylinder/bore/hex/bolt-circle radius...) it
    # is the radius of a FULL circle, which ISO dimensions as a DIAMETER, not R.
    # Mis-routing these to R both mislabels the part's main size and inflates the
    # "missed fillet" count. Round-words mark a genuine fillet; everything else
    # with a circular-feature word becomes a diameter.
    if last in ("radius", "rad", "r"):
        if any(w in n for w in ("fillet", "round", "corner", "bend",
                                "edge_radius", "blend")):
            return KIND_RADIUS, _SYM[KIND_RADIUS], PREFER_VIEWS[KIND_RADIUS]
        if any(w in n for w in ("outer", "inner", "outside", "inside", "base",
                                "disk", "disc", "cylinder", "flange", "hub",
                                "boss", "shaft", "bore", "hole", "circle",
                                "ring", "rim", "hex", "bolt", "pitch", "pcd",
                                "knob", "head", "shoulder", "neck", "barrel")):
            return KIND_DIAMETER, _SYM[KIND_DIAMETER], PREFER_VIEWS[KIND_DIAMETER]
        # bare 'radius' with no qualifier: keep as fillet R (the safe default for
        # an explicit edge-round parameter).
        return KIND_RADIUS, _SYM[KIND_RADIUS], PREFER_VIEWS[KIND_RADIUS]
    if last in _SUFFIX:
        kind = _SUFFIX[last]
        return kind, _SYM[kind], PREFER_VIEWS[kind]
    for pat, kind, sym in _RULES:
        if re.search(pat, n):
            return kind, sym, PREFER_VIEWS[kind]
    return None


def format_value(kind, symbol, value):
    """ISO-style dimension text for a value (mm or deg)."""
    if abs(value - round(value)) < 1e-6:
        v = str(int(round(value)))
    else:
        v = f"{value:.2f}".rstrip("0").rstrip(".")
    if kind == KIND_DIAMETER:
        return f"{symbol}{v}"
    if kind == KIND_RADIUS:
        return f"{symbol}{v}"
    if kind == KIND_ANGLE:
        return f"{v}{symbol}"
    if kind == KIND_CHAMFER:
        return f"C{v}"            # ISO/GB 45-deg chamfer: C<size> (= size x 45deg)
    return v


# ===========================================================================
# 3) ISO ASSEMBLY-DRAWING knowledge (装配制图)
# ===========================================================================
# An assembly drawing follows DIFFERENT rules from a part (detail) drawing:
#   - It carries NO manufacturing dimensions on the components. Components are
#     identified by ITEM BALLOONS (件号气泡, ISO 6433); only ASSEMBLY-relevant
#     dimensions are shown (overall envelope, mating/fit, mounting/installation).
#   - A PARTS LIST / BOM (零件清单, ISO 7573) sits above the title block, listing
#     every item: No. | Qty | Designation | Reference (standard) | Material.
#   - STANDARD parts (screws/washers/nuts) are NOT drawn as detail drawings;
#     they are only entered in the BOM by their ISO designation + size.
#   - NON-STANDARD parts (the part body) each get their OWN detail drawing with
#     full manufacturing dimensions.
ISO_ASSEMBLY = {
    # Item balloons — ISO 6433
    "balloon_dia": 7.0,        # balloon circle diameter (mm on paper), ~2x text_h
    "balloon_text_h": 3.5,     # item-number digit height inside the balloon
    "balloon_leader_len": 12.0,  # default leader length from feature to balloon
    "balloon_dot_r": 0.8,      # filled dot where the leader touches the component
    "balloon_gap": 9.0,        # min spacing between stacked/aligned balloons
    # Parts list / BOM — ISO 7573 (placed bottom-right, above the title block)
    "bom_row_h": 5.2,          # height of each BOM row (mm) — full, legible
    "bom_text_h": 2.5,         # BOM cell text height
    # column widths (mm): No. | Qty | Designation | Reference | Material
    "bom_cols": [10.0, 10.0, 52.0, 40.0, 28.0],
    "bom_headers": ["No.", "Qty", "Designation", "Reference", "Material"],
    "bom_order": "bottom_up",  # item 1 at the BOTTOM row, numbering upward (ISO)
    "lw_balloon": 0.35,        # balloon circle line weight (thin-medium)
    "lw_bom": 0.35,
}

# Standard-fastener ISO designations for the BOM. Keyed by the generator's
# fastener_type / class so assemble code can emit a compliant "Designation +
# Reference" pair without re-deriving the standard each time.
FASTENER_ISO = {
    "iso4762": ("Hex socket head cap screw", "ISO 4762"),   # SocketHeadCapScrew
    "iso4014": ("Hexagon head bolt", "ISO 4014"),           # HexHeadScrew
    "iso4017": ("Hexagon head screw", "ISO 4017"),
    "iso4032": ("Hexagon nut", "ISO 4032"),                 # HexNut
    "iso7089": ("Plain washer", "ISO 7089"),                # PlainWasher
    "iso7090": ("Plain washer, chamfered", "ISO 7090"),
    "iso7092": ("Washer, small series", "ISO 7092"),
    "iso10642": ("Hex socket countersunk head screw", "ISO 10642"),
    "iso7380_1": ("Button head screw", "ISO 7380-1"),
    "iso1580": ("Pan head screw", "ISO 1580"),
    "iso1207": ("Cheese head screw", "ISO 1207"),
    # nuts / inserts beyond the plain hex nut
    "din557": ("Square nut", "DIN 557"),
    "din1587": ("Domed cap nut", "DIN 1587"),
    "din1665": ("Hexagon nut with flange", "DIN 1665"),
    "heatset": ("Heat-set threaded insert", "—"),
    # bearings (reference per ISO 15 boundary dims)
    "bearing_dgbb": ("Deep groove ball bearing", "ISO 15"),
    "bearing_acbb": ("Angular contact ball bearing", "ISO 15"),
    "bearing_crb": ("Cylindrical roller bearing", "ISO 15"),
    "bearing_trb": ("Tapered roller bearing", "ISO 355"),
    # power transmission
    "sprocket": ("Chain sprocket", "ISO 606"),
    "chain": ("Roller chain", "ISO 606"),
}

DEFAULT_MATERIAL = "Steel"     # default BOM material when unknown


def fastener_designation(ftype, size):
    """BOM (Designation, Reference, size-string) for a standard fastener.
    ftype: generator fastener_type (e.g. 'iso4762'); size: 'M8-1.25' or 'M8'.
    Returns e.g. ('Hex socket head cap screw', 'ISO 4762', 'M8').
    For bearings the size string already carries bore-OD-width, kept whole."""
    name, ref = FASTENER_ISO.get(ftype, ("Fastener", ftype.upper()))
    if ftype.startswith("bearing") or ftype in ("heatset", "sprocket", "chain"):
        return name, ref, (size or "")          # keep full size descriptor
    sz = size.split("-")[0] if size else size           # M8-1.25 -> M8
    return name, ref, sz

