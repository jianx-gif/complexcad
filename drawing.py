"""
Assemble projected views into an ISO 5456-2 first-angle layout on an A3/A4 sheet.
Outputs PNG (matplotlib), SVG (matplotlib), DXF (ezdxf).

Layout (first-angle, ISO):
    +----------------------------------------+
    |  FRONT          |          ISO         |
    |                 |                       |
    |-----------------+ LEFT                  |
    |  TOP            |                       |
    +----------------------------------------+
First-angle standard relative placement:
    - FRONT  : top-left anchor
    - TOP    : directly BELOW front (aligned in X)
    - LEFT   : to the RIGHT of front (aligned in Y/height)
    - ISO    : free, placed top-right
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import ezdxf

# ISO 216 paper sizes (landscape), mm. Ordered smallest->largest: the paper
# picker walks this list and upgrades only when the content (views + dim chains +
# BOM + balloons) genuinely will not fit on the smaller sheet.
PAPER = {
    "A4": (297, 210),
    "A3": (420, 297),
    "A2": (594, 420),
    "A1": (841, 594),
}
# Order to try sheets in (small -> large).
PAPER_ORDER = ("A4", "A3", "A2", "A1")
# ISO 5457 margins: left binding margin 20, others 10
MARGIN = {"left": 20, "right": 10, "top": 10, "bottom": 10}
# ISO 7200 title block + BOM (bottom-right). The table carries the standard fields
# (Drawn/Checked/Title + projection symbol / Scale / Sheet / Drawing No) under an
# ISO 7573 parts list. It is sized to be CLEARLY LEGIBLE (~2x the earlier cramped
# 130x26 strip) yet ADAPTIVE: the picker reserves this TARGET footprint so the three
# orthographic views are placed clear of it (never crushed/overlapped), and on a
# tight sheet the table is scaled DOWN (never up past the target) just enough to fit
# without colliding -- see _table_dims(). The three views always remain the subject.
TITLEBLOCK_H = 34   # title block strip height (bottom-right) -- secondary table, kept compact
TITLEBLOCK_W = 128  # title block / BOM width -- SMALLER (table is "锦上添花"): the
                    # three views + ISO are the subject and get the freed space
# Adaptive bounds: the table may shrink toward the MIN when a small sheet has no room
# for the full target beside the views, but never grows past the target W/H above.
TITLEBLOCK_W_MIN = 100
TITLEBLOCK_H_MIN = 24
# BOM row height (mm) at the TARGET table size -- ~2x the old 5.2 so the parts-list
# text is clearly legible. Scaled down in proportion when the table is shrunk to fit.
BOM_ROW_H = 7.0

# The title block + BOM table stack must not occupy more than this fraction of the
# total sheet AREA. The default W/H/row-height above are tuned so a typical assembly
# table sits NEAR this cap (full, balanced); only an unusually long BOM that would
# exceed the cap triggers a sheet upgrade (where the same table is a smaller area
# fraction) rather than letting the table sprawl over the drawing.
TABLE_AREA_FRAC = 0.20

# Standard drawing scales (preferred, ISO 5455)
STD_SCALES = [50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]

VIEW_GAP = 12   # min gap between views (mm on paper)
GX_MAX = 36     # max inter-column gutter (mm); 3x VIEW_GAP, prevents over-spreading
ORTHO_SPAN_FRAC = 0.58   # fraction of the drawing width used by the ortho block
                         # (the rest, bottom-right, holds the ISO view)

# Max fraction of the drawing area the content may occupy on either axis.
# Above this the layout is considered too tight (views touch the frame).
FILL_MAX = 0.88

# ASSEMBLY: minimum ISO pictorial size (as a fraction of the MAIN scale) the free
# corner must be able to hold. The ISO is AUXILIARY, so we ask only for a modest
# size -- never large enough to force the main ortho views smaller. Below this the
# picker shifts the ISO to a roomier corner / sheet, but it will NOT shrink the
# views just to enlarge the ISO.
ISO_MIN_FRAC = 0.30

# Upper bound on the ISO pictorial scale, as a fraction of the MAIN (ortho) scale.
# The ISO is an AUXILIARY 3D reference and should read as smaller than the three
# orthographic views (the drawing's main subject), but it must not be a tiny dot in
# a large empty quadrant. The ISO is NOT bound to a standard scale (it is never
# dimensioned), so it grows freely to FILL its empty region up to this cap. 1.0 =
# at most the main scale; the ISO footprint is usually larger than a single ortho
# view, so even at 1.0 it reads as the auxiliary pictorial, not the main subject,
# while no longer being shrunk to a dot when a generous void is available.
ISO_MAX_FACTOR = 1.4

# Target minimum page occupancy: the smallest sheet whose best-fitting standard
# scale fills the (BOM-aware) drawing area to at least this fraction on either
# axis is preferred. The ortho views are the MAIN subject and should fill the
# sheet, so this is set HIGH -- the picker scales the views UP until they nearly
# fill the available area (capped by FILL_MAX), giving large clear views with even,
# minimal margins instead of a small block lost in whitespace.
FILL_MIN = 0.86

# ASSEMBLY top-balloon band: fraction of the frame HEIGHT that must stay clear ABOVE
# the outermost top-row balloon's rim, so the FRONT/LEFT balloons never sit on the
# upper frame line (the "balloons touch top border" bug). The reserved top band is
# the balloon's vertical reach (leader + circle) PLUS this fraction of the frame
# height, so the view block's top edge stops a visible gap below the frame.
TOP_BALLOON_FRAC = 0.09


def _balloon_reach():
    """Vertical reach (mm) of a top-row balloon ABOVE the view's top edge:
    leader length + full circle diameter (rim to rim). Single source of truth so the
    scale picker, the placement band and the renderer agree."""
    import iso_knowledge as iso
    A = iso.ISO_ASSEMBLY
    return A["balloon_leader_len"] + A["balloon_dia"]


def _top_balloon_band(edge_clear, frame_h):
    """Top clearance band (mm) reserved above the FRONT/LEFT row in ASSEMBLY layouts.
    = balloon reach + TOP_BALLOON_FRAC * frame_h, but never less than `edge_clear`
    (the symmetric balloon pad). This keeps the top-row balloon rim >= TOP_BALLOON_FRAC
    of the frame height below the upper border instead of clamped onto it."""
    if edge_clear <= 0:
        return 0.0
    return max(edge_clear, _balloon_reach() + TOP_BALLOON_FRAC * frame_h)


def _table_dims(pw, ph, n_bom):
    """ADAPTIVE size of the bottom-right table (title strip + ISO 7573 BOM).

    Returns (tb_w, tb_h, row_h, stack_h):
      tb_w   : table / title-block width (mm)
      tb_h   : title-block STRIP height (mm)
      row_h  : BOM row height (mm)
      stack_h: full stack height = tb_h + (n_bom+1) rows (title strip + BOM)

    The table is drawn at the TARGET (large, legible ~2x) size but ADAPTS so it never
    dominates the sheet or forces a needless paper upgrade:
      - WIDTH is capped at ~half the frame width (and the area cap below);
      - the full STACK HEIGHT (title strip + all BOM rows) is capped at a fraction of
        the frame height so a LONG parts list does not tower over the views -- for
        many rows the per-row height shrinks (down to a legible floor) rather than
        the stack growing without bound;
      - the whole table also respects the TABLE_AREA_FRAC (1/4-sheet) cap.
    Never scaled UP past the target. n_bom = row count (0 -> just the title strip)."""
    frame_w = pw - MARGIN["left"] - MARGIN["right"]
    frame_h = ph - MARGIN["top"] - MARGIN["bottom"]
    nb = max(0, int(n_bom))
    # --- width: target, capped at ~half the frame, never below MIN ---
    tb_w = min(TITLEBLOCK_W, 0.42 * frame_w)
    tb_w = max(TITLEBLOCK_W_MIN, tb_w)
    # --- title strip height: target, never below MIN ---
    tb_h = max(TITLEBLOCK_H_MIN, TITLEBLOCK_H)
    # --- BOM row height: target, but shrunk so the FULL stack fits a height budget ---
    row_h = BOM_ROW_H
    if nb > 0:
        nrows = nb + 1                                   # +1 header
        # the title strip + BOM stack may use at most ~48% of the frame height, so the
        # three views always keep the upper half. Shrink row_h (not the strip) to fit.
        h_budget = 0.40 * frame_h
        if tb_h + nrows * row_h > h_budget:
            row_h = max(4.8, (h_budget - tb_h) / nrows)  # legible floor 4.8 mm
    stack_h = tb_h + (nb + 1) * row_h if nb > 0 else tb_h
    # --- area cap (1/4 sheet): if still too big, shrink WIDTH (keeps rows legible) ---
    cap_area = TABLE_AREA_FRAC * pw * ph
    if tb_w * stack_h > cap_area:
        tb_w = max(TITLEBLOCK_W_MIN, cap_area / stack_h)
    return tb_w, tb_h, row_h, stack_h


# Per-view dimension-annotation buffer (mm on paper), reserved as blank space
# around each orthographic view (FRONT/TOP/LEFT) for later dimensioning. The
# value adapts to model complexity via cadquery_ops_count. ISO gets no buffer.
DIM_BUFFER_TABLE = [(10, 6.0), (30, 10.0), (float("inf"), 14.0)]  # (ops<=, buffer mm)


def dim_buffer(ops_count):
    """Return the per-view dimension buffer (mm) for a given ops complexity.
    ops_count is None -> 0 (back-compat: no reservation)."""
    if ops_count is None:
        return 0.0
    for thresh, buf in DIM_BUFFER_TABLE:
        if ops_count <= thresh:
            return buf
    return DIM_BUFFER_TABLE[-1][1]


# Max number of stacked horizontal-dimension levels we reserve frame clearance
# for. The chain-pack keeps most stacks at 1-3 levels; reserving 3 covers the
# common deep case (overall + two feature tiers) without over-pushing layouts.
DIM_CHAIN_MAX_LEVELS = 3


def dim_chain_depth(levels=DIM_CHAIN_MAX_LEVELS):
    """Vertical depth (mm on paper) a horizontal dimension CHAIN occupies on one
    side of a view: from the view outline out to the TOP of the outermost level's
    text. Used to reserve frame clearance so the chain (esp. the overall dim) does
    not run past the sheet border. Mirrors the geometry in _build_dimensions /
    annotate.edge_dim: baseline = dim_offset + (lvl)*dim_step above the outline,
    text drawn text_gap+text_h above the baseline, plus a small safety margin."""
    import iso_knowledge as iso
    K = iso.ISO129
    n = max(1, int(levels))
    return (K["dim_offset"] + (n - 1) * K["dim_step"]
            + K["text_gap"] + K["text_h"] + 1.0)


# Upper bound on stacked levels we will reserve space for, so a pathological part
# (dozens of coincident params) cannot demand an absurd reserve and crush the view.
DIM_LEVELS_CAP = 4


def estimate_dim_levels(matched, overall):
    """Estimate how many stacked dimension LEVELS each side of the ortho block
    will carry, so the layout can reserve just-enough frame clearance (and the
    scale picker can shrink/upsize only when the chains genuinely will not fit).

    Mirrors the side assignment in _build_dimensions:
      - horizontal dims: FRONT/LEFT stack ABOVE (top reserve), TOP stacks BELOW
        (bottom reserve);
      - vertical dims: all stack to the RIGHT (right reserve).
    Counts DISTINCT displayed texts per (view, orient) -- the dedup + chain-pack
    in _build_dimensions can only REDUCE levels below this, so it is a safe upper
    bound. Returns (top_levels, bot_levels, right_levels)."""
    import iso_knowledge as iso
    H_KINDS = {iso.KIND_LINEAR_H}
    V_KINDS = {iso.KIND_LINEAR_V, iso.KIND_DEPTH}
    # (view, orient) -> set of displayed texts
    seen = {}
    def add(view, orient, text):
        seen.setdefault((view, orient), set()).add(str(text))
    for od in (overall or []):
        add(od["view"], od["orient"], od["text"])
    for mm in (matched or []):
        k = mm.get("kind")
        v = mm.get("view")
        if v is None:
            continue
        if k in H_KINDS:
            orient = "h"
        elif k in V_KINDS:
            orient = "v"
        elif k == iso.KIND_POSITION:
            edge = mm.get("edge")
            if not edge:
                continue
            orient = "h" if abs(edge[3] - edge[1]) <= abs(edge[2] - edge[0]) else "v"
        else:
            continue
        add(v, orient, mm.get("text"))
    # FRONT/LEFT horizontal -> ABOVE; TOP horizontal -> BELOW; all vertical -> RIGHT.
    top_lv = max(len(seen.get(("front", "h"), ())), len(seen.get(("left", "h"), ())))
    bot_lv = len(seen.get(("top", "h"), ()))
    right_lv = max((len(seen.get((v, "v"), ())) for v in ("front", "top", "left")),
                   default=0)
    cap = DIM_LEVELS_CAP
    return (min(top_lv, cap), min(bot_lv, cap), min(right_lv, cap))


def _iso_scale(s, ih_, fw, fh, iw_=None, region_w=None, region_h=None,
               max_factor=1.0):
    """Secondary (sub-)scale for the ISO view. The ISO is a PICTORIAL aid (labelled
    'ISO', never dimensioned), so it is NOT bound to a standard scale: snapping it
    to the next std scale down throws away up to ~2.5x of the available band and
    leaves it a tiny dot. Instead we let it grow to FILL its region directly --
    the largest factor that fits both region dimensions -- capped at `max_factor` x
    the MAIN scale and with a small inset so it never touches the band edges.
    For PARTS max_factor=1 (the pictorial is not larger than the dimensioned ortho
    views). For ASSEMBLIES the ortho views are often small (a thin plate + tiny
    fasteners) and the part-identification ISO benefits from being a touch larger to
    fill an otherwise empty quadrant, so the caller may pass max_factor>1."""
    if iw_ is None:
        iw_ = ((fw * fw + fh * fh) ** 0.5)      # fallback footprint
    fits = [s * max_factor]                      # cap relative to the main scale
    inset = 0.92                                 # leave ~8% margin inside the band
    if region_w is not None and iw_ > 1e-6:
        fits.append(region_w * inset / iw_)
    if region_h is not None and ih_ > 1e-6:
        fits.append(region_h * inset / ih_)
    return max(min(fits), 1e-6)


def _extent(view):
    xs, ys = [], []
    for pl in view["visible"] + view["hidden"]:
        for (x, y) in pl:
            xs.append(x); ys.append(y)
    if not xs:
        return 0, 0, 0, 0, 0, 0
    return min(xs), min(ys), max(xs), max(ys), (max(xs)-min(xs)), (max(ys)-min(ys))


def plan_layout(views):
    """
    Compute model-space sizes of each view and the bounding footprint of the
    first-angle arrangement (front/top/left), plus iso block.
    Returns dict of per-view local size and the overall arrangement size (model mm).
    """
    ext = {k: _extent(v) for k, v in views.items()}
    fw, fh = ext["front"][4], ext["front"][5]
    tw, th = ext["top"][4], ext["top"][5]
    lw, lh = ext["left"][4], ext["left"][5]
    iw, ih = ext["iso"][4], ext["iso"][5]

    # arrangement footprint of the 3 ortho views (model mm, before scale)
    # width = front width + gap + left width ; but top sits under front
    ortho_w = max(fw, tw) + VIEW_GAP + lw
    ortho_h = max(fh, lh) + VIEW_GAP + th
    return ext, ortho_w, ortho_h, (iw, ih)


def _content_dims(ext, s, buffer, s_iso=None, reserves=(0.0, 0.0, 0.0)):
    """Scaled paper-space footprint (mm), matching the actual layout in
    _placements: the ORTHO block is two columns (front/top + left, each with a
    2*b dim buffer); the ISO view sits separately in the bottom-right.
    `reserves` = (top, bottom, right) ADDITIVE (unscaled) blank bands for the
    dimension CHAINS that stack ABOVE the FRONT/LEFT row, BELOW the TOP row, and
    to the RIGHT of the views. Reserving them here makes the scale picker shrink
    (or upsize to A3) only when the chains genuinely will not fit -- so the
    overall dimension is never silently dropped.
    Returns (ortho_w, ortho_h, iso_w, iso_h). ISO uses s_iso (defaults to s)."""
    fw, fh = ext["front"][4], ext["front"][5]
    tw, th = ext["top"][4], ext["top"][5]
    lw, lh = ext["left"][4], ext["left"][5]
    iw, ih = ext["iso"][4], ext["iso"][5]
    b = buffer
    r_top, r_bot, r_right = reserves
    si = s if s_iso is None else s_iso
    col0_w = max(fw, tw) * s + 2 * b
    col1_w = lw * s + 2 * b
    # the right reserve sits beyond the rightmost (LEFT) column's vertical dims
    ortho_w = col0_w + VIEW_GAP + col1_w + r_right
    # the top reserve sits above the upper row, the bottom reserve below the lower
    upper_h = max(fh * s + 2 * b, lh * s + 2 * b)
    lower_h = th * s + 2 * b
    ortho_h = upper_h + VIEW_GAP + lower_h + r_top + r_bot
    return ortho_w, ortho_h, iw * si, ih * si


def pick_paper_and_scale(views, buffer=0.0, reserves=(0.0, 0.0, 0.0),
                         fill_max=FILL_MAX, n_bom=0, has_table=False,
                         edge_clear=0.0, want_iso=False):
    """Choose (paper, scale). The bottom-right table (title strip + ISO 7573 BOM of
    `n_bom` rows) is sized ADAPTIVELY per candidate sheet via _table_dims(), so its
    reserved footprint shrinks on a small sheet rather than forcing a needless
    upgrade. `has_table` is True whenever a title block is present (parts always have
    one). `edge_clear` is the balloon clearance band added around the ortho block on
    every side. `want_iso` (assembly) asks the picker to also leave an empty quadrant
    for the (now small) ISO pictorial.

    The fundamental fit test models the real layout: the bottom-right corner is
    occupied by the title block + BOM (width TITLEBLOCK_W). The ortho block is
    left-biased, so it may use the FULL width only in the height ABOVE that
    bottom-right stack; where it overlaps the BOM column horizontally, the usable
    height is reduced by `bom_h`. We upgrade A4->A3->A2->A1 until a standard scale
    fits this constraint with the requested whitespace."""
    ext, ortho_w, ortho_h, (iw, ih) = plan_layout(views)

    # Pass 1: among ALL (paper, std-scale) candidates that fit AND keep the fill
    # ratio <= fill_max, pick the LARGEST scale (don't shrink a part just to fit
    # the smaller sheet); ties broken toward the smaller sheet (A4 visited first).
    # `reserves` (top/bottom/right dim-chain bands) are counted into the footprint
    # so a deep chain forces a smaller scale / A3 rather than overflowing the frame
    # or dropping the overall dimension. ASSEMBLY drawings pass a SMALLER fill_max
    # so a sheet that is too full (no room for the ISO pictorial) is rejected in
    # favour of A3 -- the views stay the same scale but gain an empty quadrant for
    # a large ISO.
    fit_fallback = None   # largest scale that merely fits, ignoring fill_max
    # Balloon clearance contributes blank space around the block, but balloons sit
    # in the OUTER margin band and overlap the page margins, so we do NOT subtract
    # the full clearance twice from the fittable area (that crushed the scale when
    # combined with a long BOM). Reserve a modest single-band allowance.
    ec_fit = edge_clear * 0.5
    ec2 = 2 * ec_fit
    is_asm = want_iso or n_bom > 0
    # Per-paper bookkeeping:
    #   soft_best  : largest scale that ALSO satisfies the FILL_MAX soft cap (used
    #                for PARTS, preserving their tuned behaviour) -> (scale, fill).
    #   hard_best  : largest scale that merely HARD-FITS (no overflow / overlap,
    #                ISO room satisfied) regardless of FILL_MAX -> (scale, fill).
    #                Used for ASSEMBLIES so the ortho views fill the sheet (the
    #                largest standard scale that physically fits is taken, not a
    #                smaller one that merely leaves more whitespace).
    per_paper_soft = {}   # paper -> (scale, fill)
    per_paper_hard = {}   # paper -> (scale, fill)
    for paper in PAPER_ORDER:
        pw, ph = PAPER[paper]
        avail_w = pw - MARGIN["left"] - MARGIN["right"]
        avail_h = ph - MARGIN["top"] - MARGIN["bottom"]
        # ADAPTIVE table footprint for THIS sheet (title strip + BOM, already scaled
        # down to respect the area / width caps on a small sheet).
        if has_table:
            tb_w, _tb_h, _rh, bom_h = _table_dims(pw, ph, n_bom)
        else:
            tb_w = bom_h = 0.0
        # 1/4-AREA RULE: the (adaptive) table stack must not exceed TABLE_AREA_FRAC of
        # the sheet area. _table_dims already shrinks toward this cap, so a violation
        # here means even the MIN-size table is too big -> upgrade to a larger sheet.
        if has_table and tb_w * bom_h > TABLE_AREA_FRAC * pw * ph + 1e-6:
            continue
        # Right column claimed by the title block + BOM stack (bottom-right).
        tb_left = pw - MARGIN["right"] - tb_w
        # EXTRA top balloon band reserved for THIS sheet (assemblies only): the top
        # band keeps the top-row balloons a fraction of the frame height below the
        # upper border. Only the amount BEYOND the symmetric ec2 pad is added to the
        # vertical footprint, so a tall block is scaled DOWN enough to leave that gap
        # (this is what stops the views topping out and the balloons hitting the frame).
        top_extra = (_top_balloon_band(edge_clear, avail_h) - edge_clear) \
            if edge_clear > 0 else 0.0
        p_soft = None
        p_hard = None
        for s in STD_SCALES:
            ow, oh, _, _ = _content_dims(ext, s, buffer, s, reserves)
            owb, ohb = ow + ec2, oh + ec2 + top_extra
            if owb > avail_w:
                continue
            # Vertical fit must respect the bottom-right table stack. The ortho
            # block is TWO columns: col0 (FRONT over TOP) is the only FULL-HEIGHT
            # column (TOP is the lowest view); col1 (LEFT) lives ONLY in the upper
            # row, ABOVE the table band. So the usable height is reduced by bom_h
            # ONLY when the FULL-HEIGHT col0 reaches the table column horizontally
            # -- col1 may overlap the table column without conflict because it sits
            # above the BOM. Using col0 (not the whole block) here is what lets a
            # COMPACT part scale UP: its narrow FRONT/TOP column stays left of the
            # table, so the views get the FULL sheet height instead of being
            # crushed by a phantom bom_h subtraction. (Mirrors `col0_into_bom` in
            # _placements, keeping the fit model and the real layout consistent.)
            block_left = MARGIN["left"]
            fw_, fh_ = ext["front"][4], ext["front"][5]
            tw_, th_ = ext["top"][4], ext["top"][5]
            col0_w_s = max(fw_, tw_) * s + 2 * buffer
            into_bom = bom_h > 0 and (block_left + col0_w_s + ec_fit
                                      > tb_left - VIEW_GAP)
            avail_h_eff = avail_h - (bom_h if into_bom else 0.0)
            if ohb > avail_h_eff:
                continue
            if fit_fallback is None or s > fit_fallback[0]:
                fit_fallback = (s, paper)
            owv, ohv, _, _ = _content_dims(ext, s, buffer, s)   # no reserve
            owvb, ohvb = owv + ec2, ohv + ec2
            # linework occupancy against the EFFECTIVE (BOM-aware) area.
            fill = max(owvb / avail_w, ohvb / max(avail_h_eff, 1e-6))
            # DIM-DENSITY (PARTS): a dimension-DENSE part carries deep horizontal dim
            # chains above FRONT/LEFT, below TOP, and vertical dims to the right (the
            # `reserves` bands). At a large scale these chains pack tightly BETWEEN the
            # views and collide with the linework / each other (the test-1 tangle). The
            # linework-only `fill` (above) is blind to this: a part can be only ~0.77
            # "full" of linework yet have its remaining space entirely consumed by dim
            # chains, so the soft cap never triggers and the picker keeps the too-large
            # 1:1. So for PARTS we also measure the RESERVE-INCLUSIVE occupancy -- the
            # views PLUS their dim bands against the usable area -- and take the larger
            # of the two as the fill the soft cap sees. When the chains are deep this
            # raises the effective fill past FILL_MAX at the big scale, dropping the
            # picker one standard scale (e.g. 1:1 -> 1:2) so the chains gain breathing
            # room. A part with shallow/no chains is unaffected (reserve ~ linework).
            if not is_asm and reserves != (0.0, 0.0, 0.0):
                fill_res = max(owb / avail_w, ohb / max(avail_h_eff, 1e-6))
                fill = max(fill, fill_res)
            # ASSEMBLY ISO ROOM -- INFORMATIONAL ONLY, NEVER A VETO.
            # The THREE ORTHO VIEWS are the drawing's subject; the ISO pictorial is a
            # SMALL auxiliary that must YIELD to them. We therefore DO NOT let "is
            # there a free quadrant for the ISO?" disqualify a (larger) main scale --
            # that was the old bug: a 1:1 view that filled the sheet left no quadrant,
            # so iso_ok rejected it and the picker fell back to a tiny 1:2, drawing the
            # part small. Instead the main scale is chosen purely on whether the ortho
            # block (+ dim/balloon/table margins) physically fits; the ISO then takes
            # whatever residual space remains downstream (its placement/scale search in
            # plan_assembly() already shrinks it into the largest empty quadrant and
            # caps it at ISO_MAX_FACTOR x the main scale). We still COMPUTE whether a
            # comfortable quadrant exists, but only as a tie-break preference, not a
            # gate: among equally-large hard-fit scales we lean toward one that leaves
            # ISO room, yet we NEVER shrink the views to manufacture that room.
            iso_ok = True
            if want_iso:
                free_w = avail_w - owb
                free_h_below = avail_h_eff - (ohb - ec2)  # below block, above BOM
                iso_w_s = iw * s * ISO_MAX_FACTOR
                iso_h_s = ih * s * ISO_MAX_FACTOR
                ok_right = (free_w >= ISO_MIN_FRAC * iso_w_s + VIEW_GAP and
                            avail_h_eff >= ISO_MIN_FRAC * iso_h_s)
                ok_below = (free_h_below >= ISO_MIN_FRAC * iso_h_s + VIEW_GAP and
                            (avail_w - (owb - ec2)) >= ISO_MIN_FRAC * iso_w_s)
                iso_ok = ok_right or ok_below
            # HARD-fit candidate: the LARGEST scale whose ortho block physically fits
            # (overflow / overlap / table only). ISO room is NOT required here -- the
            # views fill the sheet first; the ISO yields. iso_ok is recorded only so a
            # tie between two equally-large scales can prefer the one with ISO room.
            if p_hard is None or s > p_hard[0] or (s == p_hard[0]
                                                   and iso_ok and not p_hard[2]):
                p_hard = (s, fill, iso_ok)
            # SOFT candidate also respects the FILL_MAX breathing cap.
            if fill <= fill_max and (p_soft is None or s > p_soft[0]):
                p_soft = (s, fill)
        if p_soft is not None:
            per_paper_soft[paper] = p_soft
        if p_hard is not None:
            per_paper_hard[paper] = p_hard

    best = None
    if not is_asm:
        # PARTS: preserve the original behaviour exactly -- among all (paper, scale)
        # candidates that fit and satisfy fill_max, pick the LARGEST scale; ties
        # broken toward the SMALLER sheet. Restricted to the original A4/A3 pair.
        for paper in ("A4", "A3"):
            if paper in per_paper_soft and (best is None
                                            or per_paper_soft[paper][0] > best[0]):
                best = (per_paper_soft[paper][0], paper)
        # DIM-DENSE PART: keep it on the SMALLER sheet at the smaller scale rather than
        # upgrading the paper. The normal rule ("don't shrink a part just to fit the
        # smaller sheet") would pull a dimension-dense part onto A3 at the larger scale
        # -- but for a dense part the smaller scale is exactly what we WANT (it is what
        # gives the chains breathing room; the test-1 fix). So when the part carries
        # deep dim chains AND A4 holds it at a fill-cap-satisfying (already smaller)
        # scale, take that A4 candidate instead of the A3 upgrade. Parts with shallow/
        # no chains keep the original A4/A3 largest-scale behaviour untouched.
        DENSE_RESERVE = 30.0   # mm: a chain band this deep => "dimension-dense"
        dense = max(reserves) >= DENSE_RESERVE
        if dense and "A4" in per_paper_soft and best is not None and best[1] != "A4":
            best = (per_paper_soft["A4"][0], "A4")
    else:
        # ASSEMBLIES: the THREE ORTHO VIEWS are the SUBJECT and must be drawn as LARGE
        # as the sheet allows -- a too-small scale (the old 1:2 on a near-empty A4) is
        # the bug we are fixing. Each candidate's `fill` is the views' occupancy of the
        # (BOM/balloon-aware) usable area on the binding axis, i.e. exactly "how much of
        # the sheet the three views cover". So we MAXIMISE fill: the views dominate the
        # sheet and the whitespace shrinks. Two guards keep this sane:
        #   * PREFER THE SMALLER SHEET: walking small->large, we only ADOPT a larger
        #     sheet if it improves the fill by a real margin (FILL_UPGRADE_GAIN). A
        #     larger sheet that merely surrounds the same-size views with more
        #     whitespace (equal-or-worse fill) is rejected -- "don't upgrade the sheet
        #     just for whitespace". This keeps a part whose small sheet is already
        #     well filled (e.g. A4 @ 0.94) on that small sheet.
        #   * A1 is NOT entered in the normal selection (mirroring the A4/A3 cap used
        #     for parts): an A1 is reached only via the fallback passes below when even
        #     A2 cannot physically hold the block. This stops a tiny fastener assembly
        #     being magnified to 5:1 on a giant A1 just because that maximises fill.
        # NOTE: the main scale is chosen here purely on FIT + FILL of the THREE VIEWS;
        # the ISO is NOT a factor (iso_ok no longer vetoes) -- it yields downstream.
        FILL_UPGRADE_GAIN = 0.10
        SELECT_PAPERS = ("A4", "A3", "A2")
        bestf = -1.0
        for paper in SELECT_PAPERS:                    # small -> large
            if paper not in per_paper_hard:
                continue
            f = per_paper_hard[paper][1]
            if best is None or f > bestf + FILL_UPGRADE_GAIN:
                bestf = f
                best = (per_paper_hard[paper][0], paper)
        if best is None and per_paper_hard:
            # block does not fit A4/A3/A2 at any standard scale -> take the largest
            # sheet that DOES hard-fit (smallest on tie), so A1 is used only as a
            # genuine last resort rather than a fill-maximising upgrade.
            for paper in PAPER_ORDER:
                if paper in per_paper_hard:
                    best = (per_paper_hard[paper][0], paper)
                    break
    if best is not None:
        return best[1], best[0], ext, ortho_w, ortho_h, (iw, ih)
    # Pass 2: nothing satisfied FILL_MAX -> use the largest scale that merely fit.
    if fit_fallback is not None:
        return fit_fallback[1], fit_fallback[0], ext, ortho_w, ortho_h, (iw, ih)
    # Pass 3: not even a standard scale fits on any sheet -> use the LARGEST sheet
    # with a non-standard fit scale for the ortho block (the binding constraint).
    # Solve ortho_w/h(s) against the ortho region, removing the additive (unscaled)
    # buffer/gap/reserve budget AND the balloon clearance / BOM stack so the block
    # plus its bands physically fits.
    paper = PAPER_ORDER[-1]; pw, ph = PAPER[paper]
    avail_w = pw - MARGIN["left"] - MARGIN["right"] - ec2
    # conservatively assume the block reaches the BOM column -> subtract bom_h.
    avail_h = ph - MARGIN["top"] - MARGIN["bottom"] - ec2 - bom_h
    ow0, oh0, _, _ = _content_dims(ext, 0.0, buffer, 0.0, reserves)  # s=0 -> constant part
    ow1, oh1, _, _ = _content_dims(ext, 1.0, 0.0, 1.0)              # s=1, buffer=0 -> +const
    a_w = ow1 - VIEW_GAP                                   # one horizontal gap
    a_h = oh1 - VIEW_GAP                                   # one vertical gap
    sw = (avail_w - ow0) / max(a_w, 1e-6)
    sh = (avail_h - oh0) / max(a_h, 1e-6)
    s = max(min(sw, sh), 1e-6)
    return paper, s, ext, ortho_w, ortho_h, (iw, ih)


def _empty_grid(occupied_rects, frame, grid=6, cover_frac=0.18):
    """Boolean grid (row 0 = TOP) of cells that are EMPTY given OCCUPIED rectangles.
    A cell counts as occupied if rects cover >= cover_frac of its area. cover_frac
    is deliberately LOW: engineering linework / the ISO pictorial only sparsely fill
    their bounding boxes, so a cell merely TOUCHED by a view/ISO bbox is treated as
    non-void (a real drawing never renders a totally blank cell under a view)."""
    fl, fb, fr, ft = frame
    fw = fr - fl; fh = ft - fb
    n = grid
    if fw <= 0 or fh <= 0:
        return [[False] * n for _ in range(n)]
    cw = fw / n; ch = fh / n
    empty = [[True] * n for _ in range(n)]
    for r in range(n):
        cy0 = ft - (r + 1) * ch; cy1 = ft - r * ch
        for c in range(n):
            cx0 = fl + c * cw; cx1 = fl + (c + 1) * cw
            cell_area = (cx1 - cx0) * (cy1 - cy0)
            cov = 0.0
            for (rx0, ry0, rx1, ry1) in occupied_rects:
                ox = max(0.0, min(cx1, rx1) - max(cx0, rx0))
                oy = max(0.0, min(cy1, ry1) - max(cy0, ry0))
                cov += ox * oy
            if cov >= cover_frac * cell_area:
                empty[r][c] = False
    return empty


def _largest_empty_rect_cells(empty):
    """(area, r0, c0, rows, cols) of the largest all-empty rectangle in `empty`."""
    R = len(empty); C = len(empty[0]) if R else 0
    best = (0, 0, 0, 0, 0)
    heights = [0] * C
    for r in range(R):
        for c in range(C):
            heights[c] = heights[c] + 1 if empty[r][c] else 0
        stack = []
        c = 0
        while c <= C:
            h = heights[c] if c < C else 0
            start = c
            while stack and stack[-1][1] >= h:
                s_col, s_h = stack.pop()
                area = s_h * (c - s_col)
                if area > best[0]:
                    best = (area, r - s_h + 1, s_col, s_h, c - s_col)
                start = s_col
            stack.append((start, h))
            c += 1
    return best


def _max_void_2x2(occupied_rects, frame, grid=6, cover_frac=0.18):
    """Cell-area of the largest contiguous empty rectangle (see _empty_grid)."""
    return _largest_empty_rect_cells(
        _empty_grid(occupied_rects, frame, grid, cover_frac))[0]


def _placements(views, buffer=0.0, n_bom=0, has_table=False,
                reserves=(0.0, 0.0, 0.0), edge_clear=0.0, fill_max=FILL_MAX):
    """Return paper, scale, ISO sub-scale, ext, per-view placements, labels, AND the
    adaptive table dims (so the renderer draws the SAME table the layout reserved).
    `buffer` (mm) is reserved blank space around each ortho view for dimensions.
    `n_bom` is the BOM row count; `has_table` True whenever a title block is present.
    `reserves` = (top, bottom, right) dim-chain bands (mm).
    `edge_clear` (mm) is balloon clearance reserved around the ortho block.
    `fill_max` lets ASSEMBLY drawings demand more whitespace."""
    want_iso = edge_clear > 0.0          # assembly mode wants an ISO quadrant
    paper, scale, ext, ortho_w, ortho_h, (iw, ih) = pick_paper_and_scale(
        views, buffer, reserves, fill_max, n_bom, has_table, edge_clear, want_iso)
    pw, ph = PAPER[paper]
    # ADAPTIVE table dims for the CHOSEN sheet (single source of truth used by both
    # the layout below and the renderer). TB_W/TB_H = title strip; ROW_H = BOM row;
    # bom_reserve_h = height of the BOM rows ABOVE the strip; bom_h = full stack.
    if has_table:
        TB_W, TB_H, ROW_H, _stack = _table_dims(pw, ph, n_bom)
        bom_reserve_h = (n_bom + 1) * ROW_H if n_bom > 0 else 0.0
        bom_h = TB_H + bom_reserve_h
    else:
        TB_W = TB_H = ROW_H = bom_reserve_h = bom_h = 0.0
    avail_w = pw - MARGIN["left"] - MARGIN["right"]
    avail_h = ph - MARGIN["top"] - MARGIN["bottom"] - TB_H

    fw, fh = ext["front"][4], ext["front"][5]
    tw, th = ext["top"][4], ext["top"][5]
    lw, lh = ext["left"][4], ext["left"][5]
    iw_, ih_ = ext["iso"][4], ext["iso"][5]

    s = scale
    b = buffer
    avail_w_p = pw - MARGIN["left"] - MARGIN["right"]
    avail_h_p = ph - MARGIN["top"] - MARGIN["bottom"]
    # Scaled widths/heights of the three ortho views (main scale).
    fwS, fhS = fw * s, fh * s
    twS, thS = tw * s, th * s
    lwS, lhS = lw * s, lh * s
    # (ISO sub-scale s_iso is chosen later, once the real bottom-right band
    #  dimensions are known, so the ISO never overflows into the LEFT view.)

    # --- Column widths: only the TWO ortho columns share the first-angle row.
    # Col0 = front/top (front above top, left edges aligned) -> width = max(fw, tw)
    # Col1 = left view. Both carry a 2*b dim buffer. ISO is placed separately,
    # in the bottom-right corner (see below), NOT in this row.
    col0_w = max(fwS, twS) + 2 * b
    col1_w = lwS + 2 * b
    cols_w = col0_w + col1_w

    # --- Row heights (2 rows in the ortho block) ---
    # Row "front" sits above row "top". Front/left share the upper baseline.
    # Ortho rows carry a 2*b dim buffer. ISO is no longer in this block.
    upper_h = max(fhS + 2 * b, lhS + 2 * b)   # FRONT/LEFT row
    lower_h = thS + 2 * b                      # top view row

    full_w = pw - MARGIN["left"] - MARGIN["right"]
    full_h = ph - MARGIN["top"] - MARGIN["bottom"]

    # Horizontal: the two ortho columns (FRONT/TOP, then LEFT). The inter-column
    # gutter is kept modest (one VIEW_GAP..GX_MAX) so the two columns stay near the
    # LEFT of the sheet and the freed width on the RIGHT pools into one large empty
    # band for the ISO pictorial. We LEFT-BIAS the block (rather than centre it) so
    # that whole right band is contiguous -- this is what lets the ISO grow big in
    # assemblies (and is harmless for parts: the ISO then fills the right band).
    free_w = full_w - cols_w
    gx = free_w / 3.0
    # WIDTH-SPREAD: when the block is much NARROWER than the sheet, the unused width
    # pools into one big empty side band. If the ISO cannot consume it (e.g. a wide
    # TOP view leaves the void ABOVE the BOM, an awkward right-of-LEFT strip), that
    # band reads as a large void. So allow the two columns to spread further apart
    # (raise the gutter cap) to physically occupy more of the width -- the LEFT view
    # drifts right toward the BOM column, shrinking the side void. Capped so the
    # first-angle alignment still reads (FRONT over TOP, LEFT beside FRONT).
    gx_cap = GX_MAX
    if want_iso:                                    # assembly: spread to fill width
        # target: columns + gutters span up to ~78% of the available width, but the
        # LEFT column must still clear the BOM/title-block column on the right.
        usable_w = (pw - MARGIN["right"] - TB_W) - MARGIN["left"] \
            if bom_h > 0 else full_w
        spread_target = max(0.0, (min(full_w * 0.80, usable_w) - cols_w) / 2.0)
        gx_cap = max(GX_MAX, min(spread_target, free_w / 2.0))
    if gx < VIEW_GAP:
        gx = VIEW_GAP        # floor: views never touch
    elif gx > gx_cap:
        gx = gx_cap          # cap: stop columns drifting too far apart

    block_w = cols_w + 2 * gx
    # Left-bias: anchor the block near the left margin, but if it is small relative
    # to the sheet, allow a little left inset so it is not jammed against the border
    # (keeps parts looking balanced). The remaining right width feeds the ISO.
    left_inset = min((full_w - block_w) * 0.5, gx)
    x0 = MARGIN["left"] + max(0.0, left_inset)          # col0 left (left-biased)
    x1 = x0 + col0_w + gx                               # col1 left

    # Vertical: the ortho block is (upper_h + vgap + lower_h). Rather than centre
    # it geometrically (which leaves the top dim-chain short on tall parts and
    # silently drops the overall dimension), POSITION it so the chains fit:
    #   - horizontal dims on FRONT/LEFT stack ABOVE the upper row -> reserve r_top,
    #   - horizontal dims on TOP stack BELOW the lower row        -> reserve r_bot.
    # The buffer `b` is already inside each row's box on the dim side, so the
    # band still NEEDED beyond the box is (reserve - b). We place the block low
    # enough to give the top band its full need; if the available slack cannot
    # satisfy both bands at once (very tall part), the top band -- which carries
    # the OVERALL width dimension -- gets priority and the remainder goes to the
    # bottom. The scale/paper choice above already reserved this space, so on a
    # standard sheet both bands fit and nothing is dropped.
    r_top, r_bot, r_right = reserves
    top_lim = ph - MARGIN["top"]
    bot_lim = MARGIN["bottom"]
    # bands still needed OUTSIDE each row box (b already lives inside the box).
    # ASSEMBLY balloons sit OUTSIDE every view, so add their clearance to BOTH the
    # top reserve (balloons stack above FRONT/LEFT) and the bottom reserve.
    # TOP BALLOON BAND: the previous `edge_clear` (=leader+dia+6 ~ 25mm) only just
    # covered the balloon's vertical REACH above the view (leader+dia ~ 19mm), leaving
    # ~6mm to the frame -- so when the BOM-clearance lift below shoved a tall block up
    # to (top_lim - top_band), the top-row balloons landed on the frame line (the bug:
    # 0-2% top clearance). Reserve a LARGER top band that keeps the balloon's outer rim
    # at least TOP_BALLOON_FRAC of the frame height clear of the upper border, so the
    # views' top edge stops well below the frame and the balloons sit inside with a
    # visible gap. The band is only as big as the balloon reach + that fractional
    # breathing space (~8% of frame H), so the views are NOT shrunk much -- they still
    # fill the band-reduced usable height.
    top_balloon_band = _top_balloon_band(edge_clear, avail_h_p) if edge_clear > 0 else 0.0
    top_band = max(0.0, r_top - b) + max(edge_clear, top_balloon_band)
    bot_band = max(0.0, r_bot - b) + edge_clear
    # BOM-AWARE BOTTOM LIMIT: the FRONT/TOP column (col0) sits at the LEFT, but a long
    # part's TOP view can be WIDE enough that its column reaches horizontally into the
    # bottom-right BOM/title-block column. When it does, the block's BOTTOM (the TOP
    # row + its bottom dim/balloon band) must rest ABOVE the BOM stack -- otherwise the
    # TOP view's linework sweeps down into the parts list (the test-2 failure: the
    # curved tail crossing the table). So the EFFECTIVE bottom limit for both the
    # row-spread target and the base_y placement becomes the BOM top (not the sheet
    # floor) whenever col0 overlaps the table column. (The block is left-biased, so
    # only col0 -- never the LEFT column, which sits in the UPPER row above the table
    # -- governs this.) `bot_lim` stays the sheet floor for the no-overlap case.
    _tb_left_e = pw - MARGIN["right"] - TB_W
    _bom_top_e = MARGIN["bottom"] + TB_H + bom_reserve_h
    # col0 (FRONT/TOP) real right edge = left of col0 + the wider of FRONT/TOP linework.
    col0_right = x0 + (col0_w + max(fwS, twS)) / 2.0
    col0_into_bom = bom_reserve_h > 0 and col0_right > _tb_left_e - VIEW_GAP
    eff_bot_lim = max(bot_lim, _bom_top_e + VIEW_GAP) if col0_into_bom else bot_lim
    # ROW-SPREAD (assemblies): a WIDE/FLAT part is width-bound -- its views fill the
    # sheet width but are SHORT, so the ortho block occupies only the top, leaving a
    # tall empty band below (the systemic bottom void). The FRONT-above-TOP first-
    # angle relation is preserved, but the inter-row GAP is free to grow: opening it
    # spreads FRONT and TOP apart so the block spans the FULL usable height on the
    # LEFT column (where there is no BOM), filling that band with views instead of
    # whitespace. The ISO then takes the RIGHT band. We only spread when there is
    # generous slack and the block is clearly short relative to the sheet, and cap
    # the gap so the two views still read as one coordinated ortho group.
    # Now that the ISO is a SMALL auxiliary pictorial (capped < 1x), it can no longer
    # fill a large empty band on its own -- so the THREE VIEWS themselves must spread
    # to fill the sheet. We open the inter-row GAP between the FRONT/LEFT row and the
    # TOP row so the ortho block spans (most of) the usable height on the LEFT column,
    # pushing the TOP view DOWN toward the bottom margin / BOM top. FRONT-above-TOP
    # X-alignment is preserved (only the vertical gap grows); the gap is capped so the
    # two rows still read as one coordinated ortho group. This both fills the
    # left-bottom void and makes the three views dominate vertically.
    vgap = VIEW_GAP
    if want_iso:
        usable_h_left = (top_lim - top_band) - (eff_bot_lim + bot_band)
        natural_h = upper_h + VIEW_GAP + lower_h
        # spread to ~88% of the usable left-column height (leaving a small breathing
        # margin), but never beyond it.
        target_h = min(usable_h_left, 0.88 * usable_h_left + 0.12 * natural_h)
        if target_h > natural_h:
            want_gap = target_h - (upper_h + lower_h)
            # CAP the inter-row gap so the FRONT/LEFT and TOP rows stay visually
            # COORDINATED -- the gap must not become a void of its own. Limit it to
            # the taller of the two rows (so the empty band between them is never
            # larger than the views themselves) and to a sane absolute ceiling. When
            # the rows are thin (this part) this keeps them from being flung to
            # opposite ends with a hole in the middle; the leftover height then
            # stays as shared top/bottom margin instead.
            gap_ceiling = max(upper_h, lower_h) * 1.1
            vgap = max(VIEW_GAP, min(want_gap, gap_ceiling, 6.0 * VIEW_GAP))
    block_h = upper_h + vgap + lower_h
    # usable vertical span: from the sheet floor (or the BOM top, if col0 reaches the
    # table column) up to the top band. The block's bottom may not go below this floor.
    usable_bot = eff_bot_lim
    slack = (top_lim - usable_bot) - block_h   # free vertical space above the floor
    # The ISO view lives in the BOTTOM-RIGHT quadrant (below LEFT / right of TOP).
    # We bias the ortho block toward the TOP so the ISO gets a tall band below it
    # (fills the sheet vertically -> E, grows the ISO -> D). BUT the block top must
    # never reach the frame: it always clears top_band (dim chains + balloons).
    # When that bias would still leave generous slack, we DON'T slam the block to
    # the top -- we keep a balanced top margin so the FRONT/LEFT row + its balloons
    # sit clearly inside the frame and the whitespace is shared (not dumped in one
    # corner). The bottom band (TOP view dims + balloons) is also honoured.
    if slack <= 0:
        base_y = usable_bot            # part fills/exceeds height -> sit on floor
    elif top_band + bot_band >= slack:
        # tight: give the bottom its band, push the rest up (top band priority).
        base_y = max(usable_bot + bot_band, top_lim - top_band - block_h)
    else:
        # comfortable: share the leftover slack between the top and bottom margins
        # so the whitespace is BALANCED (even margins all round) rather than dumped
        # in one corner. A slight upward bias (top gets a bit less than half) keeps
        # the bottom-right quadrant generous for the ISO + BOM without leaving an
        # empty top third. The top/bottom dim+balloon bands are honoured first.
        leftover = slack - top_band - bot_band
        # Vertical bias is ADAPTIVE to how much of the height the block already fills:
        #  - TALL block (fills most of the column): bias DOWN (top margin gets the
        #    larger share) so the TOP view sinks toward the bottom/BOM and the left-
        #    bottom space is filled -- the coordinator's "push TOP down" request.
        #  - SHORT block (lots of slack, e.g. a flat plate with thin orthos): a strong
        #    down-bias would dump ALL the slack into one big TOP void. Instead CENTRE
        #    it (split the slack evenly) so the leftover becomes two small margins,
        #    each under one grid row, rather than one large continuous void.
        fill_frac = block_h / max(full_h, 1e-6)
        down_share = 0.66 if fill_frac >= 0.62 else 0.50
        top_extra = leftover * down_share
        base_y = top_lim - top_band - top_extra - block_h
    # never push the block off the sheet, nor below the usable floor (BOM top when
    # col0 reaches the table column, else the sheet floor).
    base_y = max(usable_bot, min(base_y, top_lim - block_h))

    # BOM-CLEARANCE: if the ortho block reaches horizontally into the bottom-right
    # BOM/title-block column, its BOTTOM (TOP-view row + bottom balloon band) must
    # sit ABOVE that stack, or the TOP view overlaps the parts list (the test-2
    # failure). The paper picker already upsized the sheet so this lift still leaves
    # the block inside the frame; we apply the lift here so the geometry matches.
    _tb_left = pw - MARGIN["right"] - TB_W
    _bom_top = MARGIN["bottom"] + TB_H + bom_reserve_h
    block_right_edge = x0 + block_w + edge_clear      # incl. balloon band
    if bom_reserve_h > 0 and block_right_edge > _tb_left - VIEW_GAP:
        need_bot = _bom_top + bot_band + VIEW_GAP     # block bottom must clear BOM
        if base_y < need_bot:
            base_y = min(need_bot, top_lim - top_band - block_h)
            base_y = max(bot_lim, base_y)

    # Box bottoms of each row; linework is centered inside its buffered box.
    lower_box_y = base_y                       # TOP row box bottom
    upper_box_y = base_y + lower_h + vgap       # FRONT/LEFT row box bottom (vgap may
                                                # be widened to spread a short block)
    row_top_y = lower_box_y + b                 # TOP linework baseline (b above box)
    row_front_y = upper_box_y + (upper_h - max(fhS, lhS)) / 2.0  # FRONT/LEFT baseline

    tb_top = MARGIN["bottom"] + TB_H
    tb_left = pw - MARGIN["right"] - TB_W

    # Each entry: (paper_x_of_local_minx, paper_y_of_local_miny)
    place = {}
    # FRONT: col0, upper row.
    place["front"] = (x0 + (col0_w - fwS) / 2.0, row_front_y)
    # TOP: col0, lower row, left edge aligned with FRONT's column center.
    place["top"]   = (x0 + (col0_w - twS) / 2.0, row_top_y)
    # LEFT: col1, upper row (shares FRONT baseline), centered inside its buffer.
    place["left"]  = (x1 + (col1_w - lwS) / 2.0, row_front_y)
    # ISO placement: find the LARGEST empty rectangle in the sheet that does not
    # overlap the three ortho views (with their balloon clearance), the title
    # block, or the BOM, then size the ISO to FILL it. We enumerate candidate
    # rectangles from the ACTUAL placed view linework bounds (not column widths),
    # so the ISO grabs the real free space -- typically the big bottom-right
    # quadrant -- instead of a narrow leftover band.
    tb_left = pw - MARGIN["right"] - TB_W
    bom_top = tb_top + bom_reserve_h                     # top of title block + BOM
    frame_l = MARGIN["left"]
    frame_r = pw - MARGIN["right"]
    frame_b = MARGIN["bottom"]
    frame_t = ph - MARGIN["top"]
    ec = edge_clear                                       # balloon clearance pad
    g = VIEW_GAP

    # placed linework rectangles (paper space) of the three ortho views, padded by
    # the balloon clearance so the ISO never touches a view or its balloons.
    def vrect(name, w_, h_):
        px, py = place[name]
        return (px - ec, py - ec, px + w_ + ec, py + h_ + ec)
    rF = vrect("front", fwS, fhS)
    rT = vrect("top", twS, thS)
    rL = vrect("left", lwS, lhS)
    # RAW view rects WITHOUT the balloon-clearance pad. The ISO only needs to avoid the
    # real linework (it re-pads by ISO_CLEAR when scored); reserving the full 25 mm
    # balloon band around every view as a hard no-go for candidate rectangles leaves
    # NO admissible candidate on a full sheet (NCANDS=0 -> ISO falls back to a tiny
    # corner). Candidate admissibility is therefore tested against these raw rects.
    def vrect_raw(name, w_, h_):
        px, py = place[name]
        return (px, py, px + w_, py + h_)
    rF_raw = vrect_raw("front", fwS, fhS)
    rT_raw = vrect_raw("top", twS, thS)
    rL_raw = vrect_raw("left", lwS, lhS)
    # the columns' rightmost / bottommost real extents
    top_right = rT[2]                                     # TOP linework right edge
    left_right = rL[2]                                    # LEFT linework right edge
    front_bot = rF[1]                                     # FRONT/LEFT linework bottom
    top_bot = rT[1]                                       # TOP linework bottom
    left_bot = rL[1]                                      # LEFT linework bottom
    # REAL linework edges WITHOUT the balloon clearance pad. The padded rects (rT/rL)
    # reserve a 25 mm balloon band on every side; using that band as the LEFT wall of
    # an ISO candidate double-counts clearance (the ISO score already re-pads by
    # ISO_CLEAR), needlessly shrinking the lower-right void when a wide TOP view's
    # padded box crosses the table column. For candidates that sit BELOW the views
    # (not in the balloon band) a smaller VIEW_GAP is the honest wall.
    top_right_raw = rT[2] - ec + g                        # TOP real right edge + gap
    left_bot_raw = rL[1] + ec - g                         # LEFT real bottom - gap

    # TABLE OBSTACLE: the title-block + BOM stack pinned in the bottom-right corner.
    # The ISO must NEVER overlap it (the #1 bug: ISO rendered tiny inside the table's
    # top-left, hiding the "No." header). Padded by VIEW_GAP so the ISO keeps clear.
    tbl_obst = (tb_left - g, frame_b, frame_r, bom_top + g) if bom_reserve_h > 0 \
        else None

    # candidate empty rectangles (x0, x1, y0, y1), each clamped to the frame.
    # CRITICAL: each rectangle must not intersect ANY ortho-view rect (rF/rT/rL) NOR
    # the pinned bottom-right table. We enumerate by which views bound them, then a
    # final guard drops/clips any that still overlaps (belt-and-braces).
    cands = []
    def _hit(x0c, x1c, y0c, y1c, r):
        return not (x1c <= r[0] or x0c >= r[2] or y1c <= r[1] or y0c >= r[3])
    def add(x0c, x1c, y0c, y1c):
        x0c = max(x0c, frame_l + g); x1c = min(x1c, frame_r - g)
        y0c = max(y0c, frame_b + g); y1c = min(y1c, frame_t - g)
        # CLIP against the pinned table: if this rect dips into the table's row band
        # (y below the BOM top) while reaching into the table column, pull its right
        # edge back to the table's left so it cannot overlap the parts list. If that
        # leaves it too narrow there, also try raising its floor to the BOM top.
        if tbl_obst is not None and _hit(x0c, x1c, y0c, y1c, tbl_obst):
            clipped_r = min(x1c, tbl_obst[0])            # keep left of the table
            if clipped_r - x0c >= 8.0:
                x1c = clipped_r
            else:
                y0c = max(y0c, tbl_obst[3])              # else sit ABOVE the table
        if x1c - x0c <= 8.0 or y1c - y0c <= 8.0:
            return
        # reject overlap against the RAW linework, not the padded balloon box: the ISO
        # keeps its own ISO_CLEAR margin at scoring time, so reserving the whole balloon
        # band here would reject every candidate on a full sheet (NCANDS=0). The raw
        # rects let a candidate occupy the real void between wide views and the table.
        for r in (rF_raw, rT_raw, rL_raw):
            if _hit(x0c, x1c, y0c, y1c, r):
                return
        if tbl_obst is not None and _hit(x0c, x1c, y0c, y1c, tbl_obst):
            return                                       # still hits table -> drop
        cands.append((x0c, x1c, y0c, y1c))

    # 1) FULL-HEIGHT band RIGHT of BOTH upper (LEFT) and lower (TOP) views, from
    #    above the BOM to the top frame. (tall/narrow parts)
    add(max(top_right, left_right) + g, frame_r, bom_top + g, frame_t - ec)
    # 2) CENTRE-BOTTOM: right of TOP, BELOW the FRONT/LEFT row, LEFT of the title
    #    block/BOM column -> floor is the bottom margin. (the big empty quadrant)
    add(top_right + g, tb_left - g, frame_b, front_bot - g)
    # 3) BOTTOM band right of TOP, BELOW the FRONT/LEFT row, over the BOM column ->
    #    floor is the BOM top (wider, but shorter).
    add(top_right + g, frame_r, bom_top + g, front_bot - g)
    # 4) RIGHT of the LEFT view only, down to the BOM top (LEFT is usually higher/
    #    narrower than the whole upper row, so this can be wider than #1).
    add(left_right + g, frame_r, bom_top + g, frame_t - ec)
    # 5) Bottom-RIGHT over the BOM is excluded (BOM lives there); but the strip
    #    right of TOP and below TOP's bottom, full width, is free too.
    add(top_right + g, frame_r, bom_top + g, min(front_bot, top_bot) - g)
    # 6) BELOW the whole ortho block, LEFT of the BOM column, from the frame's
    #    LEFT edge to the BOM. This is the big void on WIDE/FLAT parts whose TOP
    #    view spans most of the width (so there is no room to the RIGHT of TOP):
    #    the empty band sits UNDER the views instead. Its floor is the bottom
    #    margin; its ceiling is the lowest view's bottom. Anchoring at frame_l
    #    (not top_right) lets the ISO drop into the bottom-LEFT/centre void.
    add(frame_l, tb_left - g, frame_b, min(top_bot, front_bot) - g)
    # 7) BELOW the block over the FULL width (incl. above the BOM column, whose
    #    floor is then the BOM top) -- wider but shorter than #6.
    add(frame_l, frame_r, bom_top + g, min(top_bot, front_bot) - g)
    # 8) RIGHT of TOP (using the RAW linework edge, not the padded balloon box), over
    #    the BOM TOP, up to just below the LEFT view row: the wide lower-right band that
    #    a tall LEFT view leaves free. Using top_right_raw recovers the ~25 mm the
    #    balloon pad would otherwise waste, so the ISO can grow into this band instead
    #    of the thin slot beside the LEFT view. Right wall is the frame (this band is
    #    above the BOM, so the table does not constrain it).
    add(top_right_raw, frame_r, bom_top + g, left_bot_raw)
    # 9) Same band but extended DOWN to the bottom margin left of the table column, so a
    #    square ISO can use full height instead of the short slot's width. Right wall is
    #    the table's left edge (below the BOM top the table is present).
    add(top_right_raw, tb_left - g, frame_b, left_bot_raw)
    # 10) The tall lower-right void treated as ONE rectangle from the raw TOP-right edge
    #     to the frame, from the bottom margin up to the LEFT row: below the BOM top it
    #     is clipped to the table's left edge by add(), above it reaches the frame. This
    #     is the most permissive lower-right candidate and lets the square ISO grow.
    add(top_right_raw, frame_r, frame_b, left_bot_raw)

    # ISO placement is COVERAGE-DRIVEN: the ISO is an auxiliary pictorial whose job
    # (besides identifying the part) is to FILL the largest empty quadrant so the
    # sheet has no big continuous void. So instead of merely maximising the ISO size
    # we score each candidate rectangle by the LARGEST RESIDUAL VOID it leaves: the
    # ortho views + BOM + the ISO-in-that-rect are rasterised onto a coarse grid and
    # the biggest empty 2x2+ block is measured. We pick the placement that MINIMISES
    # that residual void, breaking ties toward the LARGER ISO.
    # ISO SIZE CAP -- the ISO is an AUXILIARY pictorial and must stay CLEARLY SMALLER
    # than the orthographic views (the drawing's main subject). It is therefore
    # capped BELOW the main scale: ~0.75x. This holds for BOTH parts and assemblies
    # (an earlier 1.6x assembly cap let the ISO dwarf the three views -- wrong). The
    # ISO still drops into the largest empty quadrant, just at a sub-view size.
    is_asm = (edge_clear > 0.0) or (bom_reserve_h > 0.0)
    # ASSEMBLY ISOs may grow up to the main scale (ISO_MAX_FACTOR=1.0) to fill an
    # otherwise empty quadrant; PART ISOs must stay CLEARLY SMALLER than the three
    # dimensioned views (the part's main subject) -- cap them well below 1x so the
    # pictorial never rivals the orthographic views in size (user: part ISO too big).
    iso_max_factor = ISO_MAX_FACTOR if is_asm else 0.62
    # static occupied rects (views + BOM/title block) shared by every candidate.
    bom_rect = (tb_left, frame_b, frame_r, bom_top)        # title block + BOM stack
    static_occ = [rF, rT, rL, bom_rect]
    frame_box = (frame_l, frame_b, frame_r, frame_t)

    # A view's bounding box overstates its footprint for round / L / irregular shapes
    # (a disc leaves its box corners blank). To let the ISO drop into those genuinely
    # empty corners and grow, we measure emptiness and clearance from the views' REAL
    # projected linework (paper mm), not their bounding boxes.
    def _view_paper_pts(name):
        vl = views.get(name) or {}
        px, py = place[name]
        ox, oy = ext[name][0], ext[name][1]
        return [(px + (mx - ox) * scale, py + (my - oy) * scale)
                for seg in (vl.get("visible") or []) for (mx, my) in seg]
    _vpts = []
    for _nm in ("front", "top", "left"):
        _vpts.extend(_view_paper_pts(_nm))

    def _empty_grid_real(frame, grid):
        """Boolean empty grid from REAL view linework points + the solid BOM block."""
        fl, fb, fr, ft = frame
        fw2 = fr - fl; fh2 = ft - fb
        g_ = [[True] * grid for _ in range(grid)]
        if fw2 <= 0 or fh2 <= 0:
            return g_
        cwl = fw2 / grid; chl = fh2 / grid
        for (px, py) in _vpts:                    # row 0 = TOP
            c = int((px - fl) / cwl); r = int((ft - py) / chl)
            if 0 <= r < grid and 0 <= c < grid:
                g_[r][c] = False
        rx0, ry0, rx1, ry1 = bom_rect             # BOM solid block covers its cells
        for r in range(grid):
            cy1 = ft - r * chl; cy0 = cy1 - chl
            for c in range(grid):
                cx0 = fl + c * cwl; cx1 = cx0 + cwl
                if not (rx1 <= cx0 or rx0 >= cx1 or ry1 <= cy0 or ry0 >= cy1):
                    g_[r][c] = False
        return g_

    def _iso_at(x0c, x1c, y0c, y1c):
        """ISO scale + its centred paper rect inside candidate (x0c..x1c, y0c..y1c)."""
        rw = x1c - x0c; rh = y1c - y0c
        si = _iso_scale(s, ih_, fw, fh, iw_, rw, rh, iso_max_factor)
        iwS_ = iw_ * si; ihS_ = ih_ * si
        cx = (x0c + x1c) / 2.0
        ix0 = cx - iwS_ / 2.0
        iy0 = y0c + (rh - ihS_) / 2.0
        if iy0 < y0c:
            iy0 = y0c
        return si, (ix0, iy0, ix0 + iwS_, iy0 + ihS_)

    def _iso_fill_rect(irect):
        """An isometric pictorial does NOT fill its bounding box (a thin plate drawn
        in ISO covers maybe half of its bbox, the rest is empty corners). For a
        realistic void estimate, treat only the CENTRAL ~72% of the ISO bbox as
        'occupied' so the optimiser does not assume the bbox corners are filled."""
        ix0, iy0, ix1, iy1 = irect
        kw = (ix1 - ix0) * 0.14; kh = (iy1 - iy0) * 0.14
        return (ix0 + kw, iy0 + kh, ix1 - kw, iy1 - kh)

    # WHERE is the emptiness? Find the largest empty block from the views + BOM
    # ALONE (no ISO yet) and aim the ISO at ITS centre. This drives the ISO into
    # the genuinely empty quadrant -- whether that is bottom-left, the right band,
    # or the strip beside a small LEFT view -- instead of merely the rect that
    # yields the biggest ISO (which can sit in a corner and leave the void elsewhere).
    grid_n = 10          # finer grid to capture empty corners of round/L views
    static_empty = _empty_grid_real(frame_box, grid_n)   # from REAL linework points
    _va, _vr0, _vc0, _vrows, _vcols = _largest_empty_rect_cells(static_empty)
    cw = (frame_r - frame_l) / grid_n; ch = (frame_t - frame_b) / grid_n
    void_cx = frame_l + (_vc0 + _vcols / 2.0) * cw
    void_cy = frame_t - (_vr0 + _vrows / 2.0) * ch
    # ALWAYS add the measured LARGEST-EMPTY-RECTANGLE itself as a candidate region
    # (converted from grid cells to paper mm, then clipped to clear views+table).
    # Otherwise, for a compact part whose views fill the sheet, every hand-listed
    # candidate can collapse to a sliver and the ISO scale falls to ~0 (the bug:
    # ISO drawn 0x0 / off-frame). This guarantees a real rectangle exists.
    ler_x0 = frame_l + _vc0 * cw
    ler_x1 = frame_l + (_vc0 + _vcols) * cw
    ler_y1 = frame_t - _vr0 * ch
    ler_y0 = frame_t - (_vr0 + _vrows) * ch
    add(ler_x0, ler_x1, ler_y0, ler_y1)
    # HARD CONSTRAINTS (user: ISO must NOT overlap a view and must NOT run off the
    # frame). We reject every candidate whose ISO bbox (with a safety margin) either
    # overlaps any view rect or the BOM, or sticks outside the frame. Overlap is
    # tested on the ISO's REAL bbox (not the sparse 72%-core), so the pictorial can
    # no longer be squeezed against a neighbouring view. If no candidate is fully
    # clear (very cramped sheet), we fall back to the least-overlapping one so the
    # ISO is still drawn.
    ISO_CLEAR = max(g, 4.0)          # safety gap between ISO bbox and any view/BOM

    def _overlap_area(a, b):
        ox = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
        oy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
        return ox * oy

    def _iso_clear_of_views(irect):
        # Overlap tested on REAL view linework (a point inside the padded ISO rect =
        # the ISO sits on drawn geometry) + solid BOM area. So the ISO may occupy the
        # empty corner of a round/L view's bounding box without being rejected.
        ex = (irect[0] - ISO_CLEAR, irect[1] - ISO_CLEAR,
              irect[2] + ISO_CLEAR, irect[3] + ISO_CLEAR)
        hit = 0.0
        for (px, py) in _vpts:
            if ex[0] <= px <= ex[2] and ex[1] <= py <= ex[3]:
                hit = 1.0
                break
        return hit + _overlap_area(ex, bom_rect)

    def _off_frame(irect):
        return (irect[0] < frame_l - 0.5 or irect[2] > frame_r + 0.5 or
                irect[1] < frame_b - 0.5 or irect[3] > frame_t + 0.5)

    frame_cx = (frame_l + frame_r) / 2.0
    frame_cy = (frame_b + frame_t) / 2.0
    best = None        # (score, si, rect...)
    best_fallback = None
    for (x0c, x1c, y0c, y1c) in cands:
        si, irect = _iso_at(x0c, x1c, y0c, y1c)
        overlap = _iso_clear_of_views(irect)   # 0 => ISO fully clear of views/BOM
        off = _off_frame(irect)
        # residual void if the ISO (sparse-core) is placed here:
        resid = _max_void_2x2(static_occ + [_iso_fill_rect(irect)], frame_box, grid_n)
        icx = (irect[0] + irect[2]) / 2.0; icy = (irect[1] + irect[3]) / 2.0
        dist = (((icx - void_cx) / max(cw, 1e-6)) ** 2
                + ((icy - void_cy) / max(ch, 1e-6)) ** 2) ** 0.5
        # ISO scale is CONTINUOUS (not a standard integer ratio -- the ISO is never
        # dimensioned): it grows to fit its region. Among candidates that are fully
        # clear of the views/BOM and on-frame, we simply pick the one that yields the
        # LARGEST ISO -- this naturally fills the biggest empty area (right band beside
        # LEFT, or the bottom-right void when LEFT runs wide) without leaving a big
        # void, and never overlaps a view or the frame (user requirements).
        si_bucket = -round(si / max(s, 1e-6) / 0.05)       # finer buckets, bigger=better
        clear_ok = (overlap <= 1e-6 and not off)
        score = (0 if clear_ok else 1, si_bucket, resid, round(dist, 1), -si)
        if clear_ok and (best is None or score < best[0]):
            best = (score, si, x0c, x1c, y0c, y1c)
        # fallback ranking (used only if NO candidate is fully clear): least overlap
        fb = (overlap, off, si_bucket, resid)
        if best_fallback is None or fb < best_fallback[0]:
            best_fallback = (fb, si, x0c, x1c, y0c, y1c)
    if best is None:            # no fully-clear candidate -> least-overlapping one
        if best_fallback is not None:
            _fb, si_fb, x0f, x1f, y0f, y1f = best_fallback
            best = ((1, 1, 1, 99, 99, 99, -si_fb), si_fb, x0f, x1f, y0f, y1f)
        else:                                              # degenerate: tiny fallback
            si0, _ = _iso_at(left_right + g, frame_r, bom_top + g, frame_t - ec)
            best = ((9, 9, 9, 99, 99, 99, -si0), si0,
                    left_right + g, frame_r, bom_top + g, frame_t - ec)
    _key, s_iso, iso_region_l, iso_region_r, iso_band_bot, iso_band_top = best
    # ISO SIZE FLOOR: the ISO must always be a VISIBLE pictorial, never a dot / 0x0 /
    # off-frame (bug on compact parts where the views fill the sheet and every region
    # collapses to a sliver -> s_iso ~ 0). Enforce a floor relative to the main scale;
    # if the chosen region is too small, GROW the region around its centre (clamped to
    # the frame, kept off the table) so the floor-size ISO fits. The ISO stays an
    # auxiliary (< views) but is always clearly drawn.
    # Floor applies to ASSEMBLIES (where the collapse-to-0 bug bit); PART ISOs are
    # capped small on purpose and must not be force-grown.
    ISO_FLOOR_FRAC = 0.35
    floor_si = (ISO_FLOOR_FRAC * scale) if is_asm else 0.0
    if s_iso < floor_si:
        s_iso = floor_si
        need_w = iw_ * s_iso; need_h = ih_ * s_iso
        cx_r = (iso_region_l + iso_region_r) / 2.0
        cy_r = (iso_band_bot + iso_band_top) / 2.0
        # grow the region to at least the needed size, centred, clamped to frame and
        # kept clear of the bottom-right table column (tb_left / bom_top).
        half_w = max((iso_region_r - iso_region_l), need_w + 2 * g) / 2.0
        half_h = max((iso_band_top - iso_band_bot), need_h + 2 * g) / 2.0
        iso_region_l = max(frame_l + g, cx_r - half_w)
        iso_region_r = min(frame_r - g, cx_r + half_w)
        # avoid the table: if the region dips into the table row band, keep it left of
        # the table column OR above the BOM top.
        if cy_r < bom_top and iso_region_r > tb_left:
            iso_region_r = min(iso_region_r, tb_left - g)
        iso_band_bot = max(frame_b + g, cy_r - half_h)
        iso_band_top = min(frame_t - ec, cy_r + half_h)
        if iso_band_bot < bom_top and iso_region_r > tb_left - g:
            iso_band_bot = max(iso_band_bot, bom_top + g)
    iso_band_w = iso_region_r - iso_region_l
    iso_band_h = iso_band_top - iso_band_bot
    iwS, ihS = iw_ * s_iso, ih_ * s_iso
    iso_cx = (iso_region_l + iso_region_r) / 2.0
    iso_x = iso_cx - iwS / 2.0
    # centre the ISO in its chosen rectangle.
    iso_y = iso_band_bot + (iso_band_h - ihS) / 2.0
    if iso_y < iso_band_bot:
        iso_y = iso_band_bot

    # FINAL NON-OVERLAP GUARANTEE. The floor-grow and region centring can leave the ISO
    # touching a view (e.g. its top edge flush against the LEFT view's bottom). Enforce
    # the hard "ISO must not overlap a view" rule here, after the final size/position are
    # known. Rather than only sliding down (which strands the ISO in a narrow slot right
    # below a view), SCAN the whole lower-right region for the position that both clears
    # the views and keeps the ISO as LARGE as possible: for a few candidate sizes (from
    # the current size downward) sweep a grid of centres over the empty band below the
    # view row and take the FIRST (largest) size that has a clear placement, preferring
    # the placement nearest the empty-region centre. Last line of defence; every assembly.
    if is_asm:
        # HARD, RELIABLE non-overlap guarantee (user: never let the ISO touch a view).
        # Test against the REAL view bounding boxes with a VISIBLE gap (VIEW_GAP, not a
        # 4-5 mm hairline) so the pictorial reads as clearly separated, not merely
        # non-touching. The linework-point test can miss a flush edge where a view's
        # samples are sparse; a bbox test with a real gap cannot.
        _gap = max(VIEW_GAP, ISO_CLEAR)                    # ~12 mm visible separation
        # Each view carries a NAME LABEL ("FRONT"/"TOP"/"LEFT") ~3 mm below its bottom
        # edge; extend every view box DOWNWARD by a label band so the ISO stays clear of
        # the label text too, not just the linework (the label sits between the view and
        # the ISO band and was being overrun).
        # Each view has a name label centred below its bottom edge (~3 mm gap, ~4 mm
        # text height). The ISO must clear BOTH the linework AND that label. Model each
        # label as a small obstacle box centred under its view (labels[] is computed
        # later, so we reconstruct the anchor here: centre-x of the raw view box, ~3 mm
        # below its bottom) and add it to the obstacle set, plus extend the view box
        # itself down a little for the text height.
        _lbl = 6.0
        _lblband = 5.0
        _vboxes = list((r[0], r[1] - _lblband, r[2], r[3])
                       for r in (rF_raw, rT_raw, rL_raw))
        for r in (rF_raw, rT_raw, rL_raw):
            _cxl = (r[0] + r[2]) / 2.0
            _byl = r[1]                                     # view bottom (label above ISO)
            _vboxes.append((_cxl - 14, _byl - _lbl - 5, _cxl + 14, _byl))
        _vboxes = tuple(_vboxes)

        def _clear_at(ix, iy, iwr, ihr):
            r_ = (ix, iy, ix + iwr, iy + ihr)
            if _off_frame(r_):
                return False
            for vr in _vboxes:
                if not (ix + iwr <= vr[0] - _gap or ix >= vr[2] + _gap
                        or iy + ihr <= vr[1] - _gap or iy >= vr[3] + _gap):
                    return False
            # table (BOM + title block), pinned bottom-right, needs a gap too.
            if not (ix + iwr <= bom_rect[0] - g or ix >= bom_rect[2]
                    or iy + ihr <= bom_rect[1] or iy >= bom_rect[3] + g):
                return False
            return True

        if not _clear_at(iso_x, iso_y, iwS, ihS):
            # Scan the WHOLE frame interior for the position that (a) fully clears every
            # view + table with the visible gap and (b) keeps the ISO as large as
            # possible, preferring the spot nearest the empty-region centre. Start at the
            # current size and shrink until a clear placement exists (it always does at
            # the minimum size in some corner). This reliably moves the ISO OFF a view
            # instead of stranding it in a hairline-adjacent slot.
            sx_lo = frame_l + g
            sx_hi = frame_r - g
            sy_lo = frame_b + g
            sy_hi = frame_t - ec
            min_si3 = 0.14 * scale
            best_place = None
            # Try a sequence of clearance gaps: prefer the full visible gap, but if the
            # sheet is too full to fit even a small ISO with that gap, relax the gap
            # (down to a hairline) so a non-overlapping placement ALWAYS exists. Within
            # each gap, take the largest size that fits, nearest the void centre.
            for _try_gap in (_gap, _gap * 0.6, ISO_CLEAR, 2.0):
                def _clear_g(ix, iy, iwr, ihr, gp=_try_gap):
                    r_ = (ix, iy, ix + iwr, iy + ihr)
                    if _off_frame(r_):
                        return False
                    for vr in _vboxes:
                        if not (ix + iwr <= vr[0] - gp or ix >= vr[2] + gp
                                or iy + ihr <= vr[1] - gp or iy >= vr[3] + gp):
                            return False
                    if not (ix + iwr <= bom_rect[0] - g or ix >= bom_rect[2]
                            or iy + ihr <= bom_rect[1] or iy >= bom_rect[3] + g):
                        return False
                    return True
                si_try = s_iso
                while si_try >= min_si3 - 1e-9:
                    iwt = iw_ * si_try; iht = ih_ * si_try
                    spanx = sx_hi - sx_lo - iwt
                    spany = sy_hi - sy_lo - iht
                    if spanx >= 0 and spany >= 0:
                        nx = 24; ny = 24
                        found_here = None
                        for gxi in range(nx + 1):
                            ixt = sx_lo + spanx * (gxi / nx)
                            for gyi in range(ny + 1):
                                iyt = sy_lo + spany * (gyi / ny)
                                if _clear_g(ixt, iyt, iwt, iht):
                                    ccx = ixt + iwt / 2.0; ccy = iyt + iht / 2.0
                                    d = ((ccx - void_cx) ** 2 + (ccy - void_cy) ** 2) ** 0.5
                                    if found_here is None or d < found_here[0]:
                                        found_here = (d, ixt, iyt)
                        if found_here is not None:
                            best_place = (si_try, found_here[1], found_here[2])
                            break
                    si_try *= 0.9
                if best_place is not None:
                    break                                   # got a placement at this gap
            if best_place is not None:
                s_iso, iso_x, iso_y = best_place
                iwS, ihS = iw_ * s_iso, ih_ * s_iso
    place["iso"]   = (iso_x, iso_y)

    # --- GROUP CENTERING (assembly) -----------------------------------------
    # The view block is anchored LEFT/TOP and the BOM/title-block sits hard in the
    # bottom-right corner, so the assembled CONTENT (3 views + balloons + dim
    # chains + ISO + table) ends up shoved toward the bottom-right with a big void
    # on the top-left -> uneven margins (top 6% / bottom 0% / left 2% / right 0%).
    # ISO convention keeps the parts list in the bottom-right, so we do NOT pull the
    # table to the centre; instead we treat "views + ISO + table" as ONE rigid block,
    # measure its ink bounding box (view linework + a small pad + the directional dim
    # bands, plus the ISO and the table footprint), and TRANSLATE the whole block by a
    # single (dx, dy) so that bounding box is centred in the frame. Every element
    # moves together, so the relative layout (table bottom-right, ISO in its quadrant)
    # is preserved while the four outer margins become balanced.
    # `dx`/`dy` are stored on `table` so the renderer shifts the BOM/title-block by
    # the SAME amount (the views/ISO `place` entries are shifted in place below).
    dx = dy = 0.0
    if want_iso:
        # ink extents per view: use the LINEWORK rect (NOT padded by the balloon
        # clearance `ec`). Balloons attach to only SOME edges of each view, so padding
        # every side by `ec` would inflate the bbox on sides that carry no balloon and
        # bias the centring (e.g. a phantom left band on a part whose balloons are all
        # on top -> the block drifts left). The balloon band is roughly symmetric
        # around the view group, so centring on the linework keeps the visible result
        # balanced; a small uniform pad keeps the views off the frame.
        PAD = VIEW_GAP
        def _vink(name, w_, h_):
            px, py = place[name]
            return (px, py, px + w_, py + h_)
        ink = [_vink("front", fwS, fhS), _vink("top", twS, thS),
               _vink("left", lwS, lhS),
               (iso_x, iso_y, iso_x + iwS, iso_y + ihS)]
        top_ink = max(r[3] for r in ink) + PAD
        bot_ink = min(r[1] for r in ink) - PAD
        left_ink = min(r[0] for r in ink) - PAD
        right_ink = max(r[2] for r in ink) + PAD
        # dim chains reach beyond the linework on the top/bottom/right dim sides.
        top_ink = max(top_ink, max(rF[3], rL[3]) - ec + r_top)
        bot_ink = min(bot_ink, rT[1] + ec - r_bot)
        right_ink = max(right_ink, max(rT[2], rL[2]) - ec + r_right)
        # TABLE PINNED TO BOTTOM-RIGHT CORNER (user: assembly table must hug the
        # bottom-right like a part drawing). The table is NOT part of the centred
        # block and does NOT move with dx/dy -- it stays flush in the corner. So we
        # do NOT fold its footprint into the centring bbox (that would have pulled
        # the table inward). Instead we center only the views+ISO+dim-bands, and
        # treat the table column as an OBSTACLE: the centred block may not slide
        # right into the pinned table, so we clamp dx so the block's right ink edge
        # stays clear of the table's left edge.
        # centre the views/ISO union bbox inside the frame, then clamp.
        dx = (frame_l + frame_r) / 2.0 - (left_ink + right_ink) / 2.0
        dy = (frame_b + frame_t) / 2.0 - (bot_ink + top_ink) / 2.0
        dx = max(frame_l - left_ink, min(dx, frame_r - right_ink))
        dy = max(frame_b - bot_ink, min(dy, frame_t - top_ink))
        # Do not let the rightward/downward shift push the views' ink into the pinned
        # bottom-right table footprint. Only matters when the block reaches down beside
        # the table column; a block sitting fully above the table is unaffected.
        if bom_h > 0:
            tbl_left = tb_left
            tbl_top = bom_top
            # if the (shifted) block would overlap the table's column AND its row band,
            # cap dx so the right ink edge clears the table's left edge.
            if (bot_ink + dy) < tbl_top:                 # block descends beside table
                dx = min(dx, tbl_left - VIEW_GAP - right_ink)
                dx = max(frame_l - left_ink, dx)         # but never off the left frame
        for _k in place:
            _px, _py = place[_k]
            place[_k] = (_px + dx, _py + dy)
    # ------------------------------------------------------------------------

    # label anchor = centered horizontally under each view, just below its bottom edge
    sizes = {"front": (fw, fh), "top": (tw, th), "left": (lw, lh), "iso": (iw_, ih_)}
    vscale = {"front": s, "top": s, "left": s, "iso": s_iso}
    labels = {}
    for name, (vw, vh) in sizes.items():
        px, py = place[name]
        labels[name] = (px + vw * vscale[name] / 2.0, py - 3.0)
    # Adaptive table dims (so the renderer draws exactly what was reserved here).
    # dx/dy here are 0: the table is PINNED to the bottom-right corner (flush, like a
    # part drawing) and does NOT move with the views' group-centering shift. The views
    # were already shifted in place above; the table renderers (_frame_lines,
    # _titleblock, _build_bom) and the balloon no-go zone all read these dx/dy, so
    # keeping them 0 draws/clears the table exactly at the corner.
    table = {"tb_w": TB_W, "tb_h": TB_H, "row_h": ROW_H,
             "bom_reserve_h": bom_reserve_h, "dx": 0.0, "dy": 0.0}
    return paper, scale, s_iso, ext, place, labels, table


def _seg_iter(views, ext, place, scale_map):
    """Yield (kind, x0,y0,x1,y1) paper-space segments for all views.
    scale_map gives the per-view scale (ISO may differ from the ortho views)."""
    for name, view in views.items():
        minx, miny = ext[name][0], ext[name][1]
        ox, oy = place[name]
        sc = scale_map[name]
        for kind in ("hidden", "visible"):
            for pl in view[kind]:
                for i in range(len(pl) - 1):
                    x0 = ox + (pl[i][0] - minx) * sc
                    y0 = oy + (pl[i][1] - miny) * sc
                    x1 = ox + (pl[i+1][0] - minx) * sc
                    y1 = oy + (pl[i+1][1] - miny) * sc
                    yield name, kind, x0, y0, x1, y1


def _build_dimensions(matched, overall, ext, place, scale, s_iso, pw=None, ph=None):
    """Build paper-space dimension primitives (format-agnostic). Two tiers:
      - OVERALL dims (front W/H, top depth): drawn OUTERMOST on the view side,
        using the bbox span -> the part's key sizes are always present.
      - FEATURE dims (local edges, holes): nested inside, on their real edge.
    Each item: {'thin': lines, 'arrow': segs, 'text': (x,y,txt,rot,va,ha)}."""
    import annotate
    import iso_knowledge as iso
    K = iso.ISO129

    # usable area for annotation TEXT inside the drawing frame. Leader callouts
    # (R/Ø/C) have no other position constraint, so without this guard one on a
    # feature near the sheet border runs its shoulder text past the frame line.
    FX0 = MARGIN["left"] + 2.0
    FY0 = MARGIN["bottom"] + 2.0
    FX1 = (pw - MARGIN["right"] - 2.0) if pw else None
    FY1 = (ph - MARGIN["top"] - 2.0) if ph else None

    def _leader_text_side(ex_, tw_):
        """Which shoulder side (+1 right / -1 left / 0 default) keeps a leader's
        horizontal shoulder + text inside the frame, given the elbow x."""
        if FX1 is None:
            return 0
        if ex_ - 6.0 - tw_ < FX0:
            return 1
        if ex_ + 6.0 + tw_ > FX1:
            return -1
        return 0

    def to_paper(view, x, y):
        sc = s_iso if view == "iso" else scale
        px, py = place[view]
        return (px + (x - ext[view][0]) * sc, py + (y - ext[view][1]) * sc)

    out = []

    def vpaper(view):
        sc = s_iso if view == "iso" else scale
        px, py = place[view]
        return px, py, px + ext[view][4] * sc, py + ext[view][5] * sc

    # model axis a linear dim measures, by (view, orient) -- an overall dim and
    # a feature dim on the SAME MODEL AXIS with the same value are the same
    # physical extent even when they sit in different views (the part depth 40
    # in TOP and a width param matched in LEFT), so one of them must go.
    DIM_AXIS = {("front", "h"): "x", ("front", "v"): "z",
                ("top", "h"): "x", ("top", "v"): "y",
                ("left", "h"): "y", ("left", "v"): "z"}

    # group by (view, orient): list of (value, text, edge_paper, is_overall)
    by_side = {}
    overall_vals = {}     # (view, orient) -> list of overall MEASURED values
    overall_texts = {}    # (view, orient) -> set of overall DISPLAYED texts
    overall_ax_vals = {}  # model axis -> list of overall MEASURED values
    overall_ax_texts = {} # model axis -> set of overall DISPLAYED texts
    for od in overall:
        v = od["view"]; orient = od["orient"]
        x0, y0, x1, y1 = od["span"]
        e = to_paper(v, x0, y0) + to_paper(v, x1, y1)
        by_side.setdefault((v, orient), []).append((1e9, od["text"], e, True))
        overall_vals.setdefault((v, orient), []).append(od.get("value", 0.0))
        overall_texts.setdefault((v, orient), set()).add(str(od["text"]))
        ax = DIM_AXIS.get((v, orient))
        if ax:
            overall_ax_vals.setdefault(ax, []).append(od.get("value", 0.0))
            overall_ax_texts.setdefault(ax, set()).add(str(od["text"]))

    # circle callouts + collect feature linear dims.
    # Concentric callouts (counterbore/countersink share a centre) would stack
    # on top of each other, so group by paper centre and fan each group's
    # callouts to distinct leader angles with growing leader length.
    circ_dims = []
    for mm in matched:
        kind = mm["kind"]
        if kind in (iso.KIND_DIAMETER, iso.KIND_RADIUS) and mm.get("center"):
            v = mm["view"]; sc = s_iso if v == "iso" else scale
            pcx, pcy = to_paper(v, *mm["center"])
            rp = (mm["value"] / 2 if kind == iso.KIND_DIAMETER else mm["value"]) * sc
            # ISO 129-1 repeated-feature shorthand: a hole that repeats n times
            # in the view is labelled once as "n x ⌀d" instead of n callouts.
            text = mm["text"]
            cnt = mm.get("count", 1) or 1
            if cnt > 1:                            # holes (n x Ø) and equal rounds (n x R)
                text = f"{cnt}x {text}"
            circ_dims.append([pcx, pcy, rp, text, kind, v])
            continue
        if kind == iso.KIND_CHAMFER and mm.get("center"):
            # leader from the chamfer slant midpoint outward (away from view centre)
            v = mm["view"]
            mxp, myp = to_paper(v, *mm["center"])
            vx0, vy0, vx1, vy1 = vpaper(v)
            ccx, ccy = (vx0 + vx1) / 2, (vy0 + vy1) / 2
            ctext = mm["text"]
            ccnt = mm.get("count", 1) or 1
            if ccnt > 1:                            # repeated equal chamfers: n x C
                ctext = f"{ccnt}x {ctext}"
            # FRAME GUARD: mirror the leader when its elbow would leave the
            # frame, and flip the text side when the shoulder text would.
            dx_, dy_ = mxp - ccx, myp - ccy
            n_ = (dx_ * dx_ + dy_ * dy_) ** 0.5 or 1.0
            ux_, uy_ = dx_ / n_, dy_ / n_
            if FY1 is not None:
                ey_ = myp + 11.0 * uy_
                if (ey_ > FY1 and uy_ > 0) or (ey_ < FY0 and uy_ < 0):
                    uy_ = -uy_
            ex_ = mxp + 11.0 * ux_
            ctw = 2.2 * len(str(ctext)) + 2.0
            if FX1 is not None and ((ex_ < FX0 and ux_ < 0)
                                    or (ex_ > FX1 and ux_ > 0)):
                ux_ = -ux_
                ex_ = mxp + 11.0 * ux_
            d = annotate.chamfer_dim(mxp, myp, ux_, uy_, ctext,
                                     text_side=_leader_text_side(ex_, ctw))
            out.append({"thin": d["leader"], "arrow": d["arrows"], "text": d["text"],
                        "leader": True})
            continue
        if kind == iso.KIND_ANGLE and mm.get("angle"):
            # ISO 129-1 angular dim: arc centred on the apex (arc CENTRE), with
            # extension lines from the feature edge out to a dim arc placed just
            # OUTSIDE that edge. Directions are scale-invariant; the vertex and the
            # feature radius are scaled to paper. The vertex may sit far outside the
            # view (shallow large-radius arc) -- the extension lines then converge
            # toward it exactly as CAD draws (the user's reference).
            v = mm["view"]
            (avx, avy), d1, d2 = mm["angle"]
            pvx, pvy = to_paper(v, avx, avy)
            sc = s_iso if v == "iso" else scale
            feat_r = mm.get("feat_r", 0.0) * sc            # feature radius -> paper
            # cap the dim-arc radius so the arc + arrow + value stay inside the
            # drawing frame: the arc opens along the bisector (toward the feature),
            # so limit dim_r to the distance from the apex to the nearest frame edge
            # along that bisector, less a margin for the arrowhead/text.
            import math as _m
            bx, by = d1[0] + d2[0], d1[1] + d2[1]
            bn = _m.hypot(bx, by)
            max_r = None
            if bn > 1e-6 and pw and ph:
                bx, by = bx / bn, by / bn                  # unit bisector toward arc
                fx0, fy0 = MARGIN["left"] + 4.0, MARGIN["bottom"] + 4.0
                fx1, fy1 = pw - MARGIN["right"] - 4.0, ph - MARGIN["top"] - 4.0
                # how far the apex can travel along the bisector before leaving frame
                room = float("inf")
                if bx > 1e-6:   room = min(room, (fx1 - pvx) / bx)
                elif bx < -1e-6: room = min(room, (fx0 - pvx) / bx)
                if by > 1e-6:   room = min(room, (fy1 - pvy) / by)
                elif by < -1e-6: room = min(room, (fy0 - pvy) / by)
                if room != float("inf"):
                    max_r = max(8.0, room - (K["text_gap"] + 4.0))
            d = annotate.angle_dim(pvx, pvy, d1, d2, mm["text"],
                                   feat_r=feat_r, max_r=max_r)
            # TEXT ANTI-OVERLAP: place the value in clear space outside the arc
            # (default = bisector). If its bbox hits already-placed dimension text
            # or another view's linework, push it further out along the bisector
            # (in steps) until clear or frame-limited. Estimate the label bbox from
            # its char count (~0.62*size mm/glyph, size from K["text_h"]).
            mdx, mdy = d["mid_dir"]
            tsz = K["text_h"]
            tw_ = 0.62 * tsz * len(mm["text"]); th_ = tsz
            def _txt_bbox(cx_, cy_):
                return (cx_ - tw_ / 2, cy_ - th_ / 2, cx_ + tw_ / 2, cy_ + th_ / 2)
            def _hit(bb):
                # against other dim texts already emitted
                for o in out:
                    ot = o.get("text")
                    if not ot:
                        continue
                    ox, oy, otxt = ot[0], ot[1], ot[2]
                    ow = 0.62 * tsz * len(str(otxt)); oh = tsz
                    if (abs(bb[0] + bb[2] - 2 * ox) < (bb[2] - bb[0] + ow)
                            and abs(bb[1] + bb[3] - 2 * oy) < (bb[3] - bb[1] + oh)):
                        return True
                # against EVERY view's linework rectangle (keep value off the body)
                for vn in ("front", "top", "left"):
                    if vn not in place:
                        continue
                    vx0, vy0, vx1, vy1 = vpaper(vn)
                    if (bb[0] < vx1 and bb[2] > vx0 and bb[1] < vy1 and bb[3] > vy0):
                        return True
                return False
            tx0, ty0 = d["text"][0], d["text"][1]
            step = th_ + 1.5
            placed_t = (tx0, ty0)
            for kstep in range(0, 14):
                cand = (tx0 + mdx * step * kstep, ty0 + mdy * step * kstep)
                # keep in frame
                if pw and ph:
                    if not (MARGIN["left"] + 3 < cand[0] < pw - MARGIN["right"] - 3
                            and MARGIN["bottom"] + 3 < cand[1] < ph - MARGIN["top"] - 3):
                        break
                if not _hit(_txt_bbox(*cand)):
                    placed_t = cand
                    break
            out.append({"thin": d["dim"] + d["ext"] + d["cross"],
                        "arrow": d["arrows"],
                        "text": (placed_t[0], placed_t[1], mm["text"], 0,
                                 "center", "center")})
            continue
        edge = mm.get("edge")
        if edge is None:
            continue
        if kind == iso.KIND_LINEAR_H:
            orient = "h"
        elif kind == iso.KIND_POSITION:
            # a spacing/pitch dimension lies along its centre-to-centre edge:
            # horizontal edge (same Y) -> 'h', vertical edge (same X) -> 'v'.
            orient = "h" if abs(edge[3] - edge[1]) <= abs(edge[2] - edge[0]) else "v"
        elif kind in (iso.KIND_LINEAR_V, iso.KIND_DEPTH):
            orient = "v"
        else:
            continue
        v = mm["view"]
        # Skip a feature dim that duplicates an overall dim already on this side
        # (e.g. arm_length == the view's overall width -> same 90, don't draw twice).
        # Two checks, because the overall's MEASURED span (e.g. 83 incl. chamfers)
        # and its DISPLAYED text (snapped to the nominal 80) can differ:
        #   1) measured-value proximity catches near-equal spans;
        #   2) identical displayed TEXT catches the snap case (overall shows "80"
        #      from an 83 span while block_length=80 would also render "80").
        # Either match means the reader would see the same number twice -> drop.
        ovs = overall_vals.get((v, orient), [])
        if any(abs(mm["value"] - ov) <= max(0.5, 0.02 * ov) for ov in ovs):
            continue
        if str(mm["text"]) in overall_texts.get((v, orient), set()):
            continue
        # same check across views by MODEL AXIS: a param equal to the part's
        # overall extent along the same axis repeats that overall dim even from
        # another view (depth 40 in TOP vs a 40 width param matched in LEFT).
        ax = DIM_AXIS.get((v, orient))
        if ax:
            oaxv = overall_ax_vals.get(ax, [])
            if any(abs(mm["value"] - ov) <= max(0.5, 0.02 * ov) for ov in oaxv):
                continue
            if str(mm["text"]) in overall_ax_texts.get(ax, set()):
                continue
        e = to_paper(v, edge[0], edge[1]) + to_paper(v, edge[2], edge[3])
        ltext = mm["text"]
        lcnt = mm.get("count", 1) or 1
        if lcnt > 1:                               # repeated rect feature: n x size
            ltext = f"{lcnt}x {ltext}"
        by_side.setdefault((v, orient), []).append((mm["value"], ltext, e, False))

    # First-angle layout: put each view's horizontal dims on the side AWAY from
    # the neighbouring view so they don't fight for the gap between views.
    #   FRONT (upper-left): h-dims ABOVE, v-dims RIGHT
    #   TOP   (lower-left): h-dims BELOW, v-dims RIGHT
    #   LEFT  (upper-right): h-dims ABOVE, v-dims RIGHT
    H_SIDE = {"front": "above", "top": "below", "left": "above"}
    for (view, orient), items in by_side.items():
        items.sort(key=lambda t: t[0])     # smallest innermost, overall outermost
        # Final safety net: never stack two dimensions showing the SAME text on
        # one side. Beyond the feature-vs-overall dedup above, two feature params
        # can share a value/text (e.g. two 20 mm features along the same axis);
        # drawing both just stacks identical numbers and pushes the outermost off
        # the sheet. Keep the first (innermost after the sort) per displayed text.
        seen_text = set()
        deduped = []
        for it in items:
            t = str(it[1])
            if t in seen_text:
                continue
            seen_text.add(t)
            deduped.append(it)
        items = deduped
        vx0, vy0, vx1, vy1 = vpaper(view)
        h_above = H_SIDE.get(view, "below") == "above"
        # CHAIN-PACK the stack: dims that do not overlap along the measure axis
        # share ONE dimension line (ISO chain dimensioning) instead of each
        # taking its own level -- the stack stays shallow and reads tidy.
        # Items are sorted smallest-first, so when spans DO overlap the smaller
        # stays closer to the view (correct nesting) and the larger moves out;
        # the full-span OVERALL dims always end up outermost.
        levels = []          # per level: list of (lo, hi) occupied intervals
        placed = []          # (lvl, text, e)
        for (_val, text, e, _is_over) in items:
            if orient == "h":
                lo, hi = min(e[0], e[2]), max(e[0], e[2])
            else:
                lo, hi = min(e[1], e[3]), max(e[1], e[3])
            mid = (lo + hi) / 2.0
            tw = 2.2 * len(str(text)) + 3.0     # text footprint on the line
            ilo = min(lo, mid - tw / 2) - 1.5   # margin between chained dims
            ihi = max(hi, mid + tw / 2) + 1.5
            lvl = 0
            while lvl < len(levels) and any(ilo < b and ihi > a
                                            for (a, b) in levels[lvl]):
                lvl += 1
            if lvl == len(levels):
                levels.append([])
            levels[lvl].append((ilo, ihi))
            placed.append((lvl, text, e))
        # Step between stacked dim levels. VERTICAL stacks (orient == "v") carry
        # their value text ROTATED 90 deg and sitting to the LEFT of each baseline,
        # so neighbouring levels put two tall rotated numbers only `dim_step` apart
        # -- the innermost small thickness dims (e.g. 8/10) then read cramped
        # against each other and the part edge. Widen the step for vertical stacks
        # so each rotated number gets its own clear column, BUT only as far as the
        # free space to the right allows: the FRONT view's stack lives in the
        # column toward the LEFT view, so an over-wide step would shove its outer
        # numbers onto the LEFT-view linework. Compute the nearest rightward
        # obstacle (frame edge, or the left edge of any OTHER view whose Y-band
        # overlaps this stack's text rows) and size the step to keep the OUTERMOST
        # level inside it. Horizontal stacks already breathe (upright text spread
        # along the line), so leave those at the standard step.
        v_off = K["dim_offset"]
        v_step = K["dim_step"]
        if orient == "v" and placed:
            max_lvl = max(p[0] for p in placed)
            # nearest rightward obstacle: frame edge, or the left edge of any OTHER
            # view whose Y-band overlaps this stack's text rows. The stack's text
            # columns must stay LEFT of it.
            right_lim = (pw - MARGIN["right"] - 2.0) if pw else None
            ylo = min(min(e[1], e[3]) for (_l, _t, e) in placed)
            yhi = max(max(e[1], e[3]) for (_l, _t, e) in placed)
            for ovw in ("front", "top", "left", "iso"):
                if ovw == view or ovw not in place:
                    continue
                ox0, oy0, ox1, oy1 = vpaper(ovw)
                if ox0 > vx1 and not (oy1 < ylo - 2.0 or oy0 > yhi + 2.0):
                    cand = ox0 - 2.0
                    right_lim = cand if right_lim is None else min(right_lim, cand)
            # Target a WIDER step so each rotated number gets its own clear column
            # (decompresses the cramped inner 8/10). Fit the whole stack inside the
            # rightward obstacle:
            #  - lots of room (TOP stack -> open lower-right void): use the wide
            #    target step and a slightly larger first offset.
            #  - hard against a neighbour view (FRONT stack -> LEFT view): spread
            #    the levels EVENLY across the available room instead of letting the
            #    outermost number land on that view's linework -- an even, contained
            #    chain reads better than a wider one that collides. A small floor
            #    keeps adjacent rotated numbers separable.
            want = K["dim_step"] * 1.45
            MIN_V_STEP = 6.5
            if right_lim is not None and max_lvl > 0:
                room = right_lim - (vx1 + v_off)
                fit = room / max_lvl
                if fit >= K["dim_step"]:
                    v_step = min(want, fit)
                    v_off = K["dim_offset"] + 3.0
                else:
                    v_step = max(MIN_V_STEP, fit)     # contain within the obstacle
            else:
                v_step = want
                v_off = K["dim_offset"] + 3.0
        for (lvl, text, e) in placed:
            step = (v_off + lvl * v_step) if orient == "v" else \
                   (K["dim_offset"] + lvl * K["dim_step"])
            # Dimension TEXT occupies text_gap+text_h beyond the baseline, on the
            # side AWAY from the view (above for an upper chain, below for a lower
            # one). The guard must judge by the TEXT EDGE, not the bare baseline,
            # or the number itself crosses the frame even when the line clears it.
            text_reach = K["text_gap"] + K["text_h"]
            safety = 1.0
            if orient == "h":
                baseline = (vy1 + step) if h_above else (vy0 - step)
                # FRAME GUARD: a deep stack on a view near the sheet edge would
                # run past the border; a dimension drawn outside the frame is
                # worse than one omitted, so drop the overflowing levels. The
                # text grows AWAY from the view, so check that edge.
                text_edge = (baseline + text_reach) if h_above else (baseline - text_reach)
                if ph is not None and not (
                        MARGIN["bottom"] + safety <= text_edge
                        <= ph - MARGIN["top"] - safety):
                    continue
            else:
                baseline = vx1 + step
                # vertical dim text sits LEFT of the line (toward the view), so the
                # baseline itself is the rightmost element; guard on it directly.
                if pw is not None and baseline > pw - MARGIN["right"] - safety:
                    continue
            d = annotate.edge_dim(e[0], e[1], e[2], e[3], orient, baseline, text)
            import os as _os
            if _os.environ.get("DIM_DBG"):
                import sys as _sys
                _emid = ((e[0]+e[2])/2, (e[1]+e[3])/2)
                print(f"[DIM] {view:5s} {orient} lvl={lvl} step={step:.1f} "
                      f"baseline={baseline:.1f} txt={text!r:8s} "
                      f"edgemid=({_emid[0]:.1f},{_emid[1]:.1f}) "
                      f"txtpos=({d['text'][0]:.1f},{d['text'][1]:.1f})", file=_sys.stderr)
            out.append({"thin": d["ext"] + d["dim"], "arrow": d["arrows"], "text": d["text"]})

    # Emit circle callouts, fanning concentric ones to distinct angles so their
    # leaders/shoulders/text don't pile up at the shared centre.
    groups = []                                # [(cx, cy, [dim,...]), ...]
    for cd in circ_dims:
        cx, cy = cd[0], cd[1]
        g = next((gg for gg in groups if abs(gg[0] - cx) < 1.0
                  and abs(gg[1] - cy) < 1.0), None)
        if g is None:
            groups.append((cx, cy, [cd]))
        else:
            g[2].append(cd)
    import math
    FAN = [45, 135, 30, 150]                    # distinct leader angles per group
    for _cx, _cy, members in groups:
        members.sort(key=lambda c: c[2])        # innermost circle first
        multi = len(members) > 1                 # concentric stack -> must separate
        for i, (pcx, pcy, rp, text, kind, v) in enumerate(members):
            through = False
            # A corner-fillet RADIUS is a quarter-arc facing the nearest plate
            # CORNER, so aim its leader toward that corner (in paper space, so the
            # projection Y-flip can't mislead) -> the arrow lands on the real arc.
            if kind == iso.KIND_RADIUS:
                vx0, vy0, vx1, vy1 = vpaper(v)
                vcx, vcy = (vx0 + vx1) / 2, (vy0 + vy1) / 2
                # Is the arc CENTRE inside the view rectangle? A small corner fillet
                # has its centre ON/near the part (inside the view); a LARGE sweep/
                # profile arc (e.g. R47.5) has its centre FAR OUTSIDE the view -- so
                # aiming "outward from the view centre through the arc centre" points
                # the leader AWAY from the part and shoots it off the sheet. Decide
                # the leader direction by where the centre lies.
                center_in_view = (vx0 - 2.0 <= pcx <= vx1 + 2.0 and
                                  vy0 - 2.0 <= pcy <= vy1 + 2.0)
                if center_in_view:
                    # corner/edge round: aim OUTWARD (centre -> away from view centre)
                    # so the arrow lands on the arc facing the nearest plate corner.
                    if abs(pcx - vcx) < 1e-6 and abs(pcy - vcy) < 1e-6:
                        ang = 135.0
                    else:
                        ang = math.degrees(math.atan2(pcy - vcy, pcx - vcx))
                    # an arc centred (nearly) ON a view corner is a CONCAVE notch:
                    # run the leader THROUGH the centre to the far (inboard) arc side.
                    through = min(math.hypot(pcx - qx, pcy - qy)
                                  for qx in (vx0, vx1) for qy in (vy0, vy1)) \
                        <= 1.2 * rp
                else:
                    # large-radius arc, centre OUTSIDE the view: aim from the centre
                    # TOWARD the view centre so the arc contact point (centre + r*dir)
                    # lands on the VISIBLE arc inside the view, and the short leader
                    # stub stays inside the frame. Never run through the (off-view)
                    # centre here.
                    ang = math.degrees(math.atan2(vcy - pcy, vcx - pcx))
                    through = False
                # Alone: a single fixed-length leader to the corner. But CONCENTRIC
                # radii (e.g. R20 + R22 sharing a centre) would aim at the SAME
                # corner with the SAME length -> their text anchors overlap. When
                # the group has more than one member, stagger the leader length by
                # index so each callout's shoulder/text sits at a distinct radius
                # along the (shared) corner direction and they no longer collide.
                llen = 16.0 + (i * 9.0 if multi else 0.0)
            else:
                ang = FAN[i % len(FAN)]
                llen = 9.0 + i * 7.0            # grow so outer callouts clear inner
            # FRAME GUARD: keep the elbow inside the frame -- mirror the leader
            # direction when it would exit (skip the horizontal mirror for
            # through-centre notch leaders, whose contact side is geometric) --
            # and flip the text side when the shoulder text would cross.
            ar = math.radians(ang)
            ex_ = pcx + (rp + llen) * math.cos(ar)
            tw_ = 2.2 * len(str(text)) + 2.0
            if FX1 is not None and not through:
                if (ex_ < FX0 and math.cos(ar) < 0) \
                        or (ex_ > FX1 and math.cos(ar) > 0):
                    ang = 180.0 - ang
                    ar = math.radians(ang)
                    ex_ = pcx + (rp + llen) * math.cos(ar)
            if FY1 is not None:
                ey_ = pcy + (rp + llen) * math.sin(ar)
                if (ey_ > FY1 and math.sin(ar) > 0) \
                        or (ey_ < FY0 and math.sin(ar) < 0):
                    ang = -ang
                    ar = math.radians(ang)
                    ex_ = pcx + (rp + llen) * math.cos(ar)
            d = annotate.circle_dim(pcx, pcy, rp, text, leader_len=llen,
                                    angle_deg=ang, through_center=through,
                                    text_side=_leader_text_side(ex_, tw_))
            out.append({"thin": d["leader"], "arrow": d["arrows"], "text": d["text"],
                        "leader": True})

    # --- Final anti-overlap pass -------------------------------------------
    # The ISO placement above keeps each dimension on its correct line, but two
    # callouts for DIFFERENT features (different centres/kinds) can still have
    # their text land within a few mm of each other by coincidence (e.g. a small
    # chamfer 'C1' next to a thin-wall '2', or two fanned radii whose corner-aimed
    # leaders converge). Linear/overall dims are ISO-anchored and must NOT move;
    # only LEADER callouts (radius/diameter/chamfer) are free to slide along their
    # own leader. So: when a callout's text overlaps any earlier label, push that
    # callout's whole geometry (leader + arrow + text) radially outward, away from
    # the leader's own start, until it clears. Bounded iterations so it always
    # terminates even in a dense cluster.
    MINSEP = 5.0           # mm: labels closer than this are treated as overlapping
    STEP = 3.0             # mm: how far to slide per attempt
    MAXTRY = 6

    def _anchor(dm):
        return dm["text"][0], dm["text"][1]

    def _shift(dm, dx, dy):
        dm["thin"] = [(a + dx, b + dy, c + dx, e + dy) for (a, b, c, e) in dm["thin"]]
        dm["arrow"] = [(a + dx, b + dy, c + dx, e + dy) for (a, b, c, e) in dm["arrow"]]
        tx, ty, txt, rot, va, ha = dm["text"]
        dm["text"] = (tx + dx, ty + dy, txt, rot, va, ha)

    for i, dm in enumerate(out):
        if not dm.get("leader"):
            continue                      # only callouts may be nudged
        # slide direction = from the leader's arrow tip (feature) toward its text,
        # i.e. further OUT along the existing leader, so the arrow still points at
        # the same feature and the callout just reads from further away.
        arr = dm["arrow"]
        ax, ay = _anchor(dm)
        if arr:
            tipx, tipy = arr[0][0], arr[0][1]     # arrowhead tip = feature point
            ux, uy = ax - tipx, ay - tipy
            n = (ux * ux + uy * uy) ** 0.5 or 1.0
            ux, uy = ux / n, uy / n
        else:
            ux, uy = 1.0, 0.0
        for _try in range(MAXTRY):
            ax, ay = _anchor(dm)
            clash = False
            for j, other in enumerate(out):
                if j == i:
                    continue              # check against ALL other labels, not
                                          # just earlier ones: a movable callout
                                          # must yield to a fixed neighbour that
                                          # happens to come later in the list too.
                bx, by = _anchor(other)
                if ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 < MINSEP:
                    clash = True
                    break
            if not clash:
                break
            # never slide a callout's text out of the frame: better a close
            # pair of labels than one beyond the border.
            if FX1 is not None:
                nx, ny = ax + ux * STEP, ay + uy * STEP
                if not (FX0 <= nx <= FX1 and FY0 <= ny <= FY1):
                    break
            _shift(dm, ux * STEP, uy * STEP)
    return out


def _clip_seg(p0, p1, xmin, ymin, xmax, ymax):
    """Liang-Barsky clip of segment p0->p1 to the axis-aligned rectangle.
    Returns ((x0,y0),(x1,y1)) clipped, or None if fully outside."""
    x0, y0 = p0
    x1, y1 = p1
    dx = x1 - x0
    dy = y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0),
                 (-dy, y0 - ymin), (dy, ymax - y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return None                  # parallel and outside
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            if r > t0:
                t0 = r
        else:
            if r < t0:
                return None
            if r < t1:
                t1 = r
    return ((x0 + t0 * dx, y0 + t0 * dy), (x0 + t1 * dx, y0 + t1 * dy))


def _build_sweep_overlay(sweep, ext, place, scale, dims, pw=None, ph=None):
    """Project a swept feature's PATH into each ortho view as an ISO CENTRELINE
    (dash-dot) plus its key dimensions, and append the dimension callouts to
    `dims` (so they share the anti-overlap pass). Returns a list of centreline
    polylines [(view, [(x,y),...]), ...] in paper space.

    The path lives in posed-model coords; we map it to each view exactly like the
    model linework: project to (paper_x, paper_y), then (coord - ext_min)*scale +
    place. The path is drawn ONLY in the view where it reads as a true curve (its
    projected bounding box is largest), to avoid a degenerate edge-on line."""
    import projlib
    import annotate
    import iso_knowledge as iso
    K = iso.ISO129
    if not sweep or not sweep.get("edges3d"):
        return []

    ORTHO = ("front", "top", "left")

    def to_paper(view, x2, y2):
        sc = scale
        px, py = place[view]
        return (px + (x2 - ext[view][0]) * sc, py + (y2 - ext[view][1]) * sc)

    # Choose the view that shows the path most fully: largest projected bbox area.
    best_view, best_area = None, -1.0
    proj_cache = {}
    for v in ORTHO:
        pax, pay = projlib_view(v)
        allpts = []
        for e in sweep["edges3d"]:
            allpts += projlib.project_to_view(e["pts3d"], pax, pay)
        proj_cache[v] = allpts
        if len(allpts) < 2:
            continue
        xs = [p[0] for p in allpts]; ys = [p[1] for p in allpts]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if area > best_area:
            best_area, best_view = area, v
    if best_view is None:
        return []

    v = best_view
    pax, pay = projlib_view(v)
    # CLIP RECTANGLE: the chosen view's paper-space extent, plus a small ISO-style
    # overshoot. The 3D path is already trimmed to the solid, but its PROJECTION
    # into a given view can still run past the part's silhouette in that view (an
    # arc/edge-on spine projecting as a line beyond the model outline) and -- when
    # the view sits near the sheet border -- spill out through the frame. A
    # centreline must behave like any other: stay within the feature extent with a
    # small overshoot, never crossing the frame. So clip every projected polyline
    # to this rectangle before drawing.
    OVER = 3.0                                          # mm overshoot beyond extent
    px0, py0 = place[v]
    cx0 = px0 - OVER
    cy0 = py0 - OVER
    cx1 = px0 + ext[v][4] * scale + OVER
    cy1 = py0 + ext[v][5] * scale + OVER

    def _clip_polyline(poly):
        """Split a paper-space polyline into the sub-polylines that lie inside the
        clip rectangle (Liang-Barsky per segment, stitched back into runs)."""
        runs = []
        cur = []
        for k in range(len(poly) - 1):
            seg = _clip_seg(poly[k], poly[k + 1], cx0, cy0, cx1, cy1)
            if seg is None:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
                continue
            a, b = seg
            if not cur:
                cur = [a, b]
            elif abs(cur[-1][0] - a[0]) < 1e-6 and abs(cur[-1][1] - a[1]) < 1e-6:
                cur.append(b)                            # contiguous -> extend
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = [a, b]
        if len(cur) >= 2:
            runs.append(cur)
        return runs

    centerlines = []
    for e in sweep["edges3d"]:
        pv = projlib.project_to_view(e["pts3d"], pax, pay)
        if len(pv) < 2:
            continue
        poly = [to_paper(v, x, y) for (x, y) in pv]
        for run in _clip_polyline(poly):
            centerlines.append((v, run))

    # Dimensions: overall path LENGTH (as a note near the path mid), each ARC
    # radius (R), and helix PITCH. Drawn as simple leader-note callouts so they
    # never fight the model's linear dims; they ride the shared anti-overlap pass.
    vx0, vy0, vx1, vy1 = (place[v][0], place[v][1],
                          place[v][0] + ext[v][4] * scale,
                          place[v][1] + ext[v][5] * scale)
    notes = []
    is_helix = any(e["kind"] == "helix" for e in sweep["edges3d"])
    # OVER-DIMENSIONING / non-standard text removed (user): an arc spine is fully
    # defined by its RADIUS (R) + its SWEPT ANGLE (the °, drawn as a proper angular
    # dim). The "PATH L=..." note is a free-text annotation, NOT a compliant ISO
    # dimension, and it merely RESTATES the same arc (R + ° already give the length
    # = R*θ). So we DROP "PATH L=" for arc spines and keep only R. A non-arc spine
    # (helix uses PITCH; a free/loft spline has no single radius) still needs its
    # governing note, so PATH L is kept ONLY where there is no arc radius to carry
    # the size (free spline) and it is not a helix.
    has_arc_r = any(e["kind"] == "arc" and e.get("radius") for e in sweep["edges3d"])
    for e in sweep["edges3d"]:
        if e["kind"] == "arc" and e["radius"]:
            notes.append((f"R{_num(e['radius'])}", 1))
    if sweep.get("pitch"):
        notes.append((f"PITCH {_num(sweep['pitch'])}", 2))
    if not is_helix and not has_arc_r and not sweep.get("pitch"):
        # free/loft spine with no radius and no pitch: PATH L is the only size note
        notes.append((f"PATH L={_num(sweep['length'])}", 0))
    if not notes:
        return centerlines

    # Place the PATH notes (R.. / PITCH..) as a leadered note BLOCK in genuine CLEAR
    # space whose LEADER does not cross any OTHER view. The path lives in view `v`
    # (best_view); anchoring the block ABOVE the topmost view forced the leader to
    # run down THROUGH the FRONT view to reach the path in TOP (the R48.3 overlap).
    #
    # Strategy: the block sits in empty air NEXT TO the path's own view `v`, on the
    # side with the most room to the frame that is NOT occupied by another ortho
    # view, so the leader stays a short diagonal entirely in clear space. We test
    # candidate spots (right of v, left of v, below v, above v) and pick the first
    # whose block rectangle AND whose leader avoid every view's linework rectangle.
    if centerlines:
        anchor = centerlines[0][1][len(centerlines[0][1]) // 2]
    else:
        anchor = ((vx0 + vx1) / 2, vy1)

    fx0 = MARGIN["left"] + 3.0
    fx1 = (pw - MARGIN["right"] - 3.0) if pw else (vx1 + 80.0)
    fy0 = MARGIN["bottom"] + 3.0
    fy1 = (ph - MARGIN["top"] - 3.0) if ph else (vy1 + 60.0)

    line_h = K["text_h"] + 2.5
    block_h = len(notes) * line_h
    tw = max(2.2 * len(t) + 3.0 for (t, _s) in notes)   # widest note footprint

    # every ortho view's linework rectangle (the no-cross zones)
    vrects = []
    for vv in ORTHO:
        if vv in place:
            rx0, ry0 = place[vv]
            vrects.append((rx0, ry0, rx0 + ext[vv][4] * scale,
                           ry0 + ext[vv][5] * scale))

    def _rect_hit(bx0, by0, bx1, by1_):
        for (rx0, ry0, rx1, ry1) in vrects:
            if bx0 < rx1 and bx1 > rx0 and by0 < ry1 and by1_ > ry0:
                return True
        return False

    def _seg_hits_views(x0, y0, x1, y1):
        for t in range(1, 24):
            f = t / 24.0
            x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            for (rx0, ry0, rx1, ry1) in vrects:
                if rx0 <= x <= rx1 and ry0 <= y <= ry1:
                    return True
        return False

    # the path's own view rect (so candidates hug IT, leader short)
    vx0v, vy0v = place[v]
    vx1v = vx0v + ext[v][4] * scale
    vy1v = vy0v + ext[v][5] * scale
    GAP = K["dim_offset"] + 6.0

    # candidate block LEFT-BOTTOM positions around the path's view, in preference
    # order: right, below, above, left. Each as (bx, by_bottom).
    cands = [
        (vx1v + GAP, anchor[1] - block_h / 2.0),                 # right of view
        (anchor[0] - tw / 2.0, vy0v - GAP - block_h),            # below view
        (anchor[0] - tw / 2.0, vy1v + GAP),                     # above view
        (vx0v - GAP - tw, anchor[1] - block_h / 2.0),           # left of view
    ]
    chosen = None
    for (bx, by) in cands:
        bx = min(max(bx, fx0), fx1 - tw)
        by = min(max(by, fy0), fy1 - block_h)
        # leader from the block edge nearest the anchor to the path midpoint
        lx = bx if bx >= anchor[0] else bx + tw
        ly = min(max(anchor[1], by), by + block_h)
        if _rect_hit(bx, by, bx + tw, by + block_h):
            continue
        if _seg_hits_views(lx, ly, anchor[0], anchor[1]):
            continue
        chosen = (bx, by, lx, ly)
        break
    if chosen is None:
        # fallback: right of the view, clamped (accept a short crossing rather than
        # dropping the note); better than piling onto another view's dims.
        bx = min(max(vx1v + GAP, fx0), fx1 - tw)
        by = min(max(anchor[1] - block_h / 2.0, fy0), fy1 - block_h)
        chosen = (bx, by, bx, anchor[1])
    bx, by, lx, ly = chosen
    ha = "left"
    for i, (txt, _slot) in enumerate(notes):
        ty = by + block_h - (i + 1) * line_h + line_h * 0.5
        leader = [(lx, ly, anchor[0], anchor[1])] if i == 0 else []
        dims.append({"thin": leader, "arrow": [],
                     "text": (bx, ty, txt, 0, "center", ha),
                     "leader": False})
    return centerlines


def projlib_view(v):
    import projlib
    return projlib.VIEWS[v]["paper_x"], projlib.VIEWS[v]["paper_y"]


def render(views, uuid, out_prefix, fmts=("png", "svg", "dxf"), proj="first-angle",
           ops_count=None, matched=None, overall=None, sweep=None, section=None,
           bom=None, balloons=None, axes=None, bearings=None, threads=None,
           mass=None, title=None):
    """bom/balloons set ASSEMBLY-drawing mode (ISO):
      balloons: [{"view","x","y","item"}] feature points (model-view coords) to
                tag with an ISO 6433 item balloon.
      bom: [{"item","qty","designation","reference","material"}] parts list
           rendered as an ISO 7573 table above the title block.
    ISO standard-part conventional representations (assembly drawings):
      bearings: ISO 8826-1 simplified rolling-bearing symbols. Each entry, in the
                target view's model-view coords:
                  {"view", "cx","cy", "od", "bore", "width", "end_on",
                   "ax","ay"}  -- ax,ay = unit axis direction projected in-view
                                 (only used when not end_on, to orient the box).
      threads:  ISO 6410 conventional thread lines. Each entry, in model-view
                coords: a SIDE view minor-diameter pair {"view","x0","y0","x1","y1"}
                (one thin line per side, two entries per thread), or an END view
                {"view","end_on":True,"cx","cy","r"} for the 3/4 minor-dia arc.
    When given, component manufacturing dims are expected to be omitted by the
    caller (only assembly dims passed in `matched`/`overall`)."""
    buffer = dim_buffer(ops_count)
    # Bottom-right table: a title block is ALWAYS present; assemblies add an ISO 7573
    # BOM of len(bom) rows. The table is sized adaptively inside _placements.
    n_bom = len(bom) if bom else 0
    has_table = True
    # DIMENSION-CHAIN reserves: estimate how deep the horizontal chains stack on
    # the top (FRONT/LEFT) and bottom (TOP) sides and how far the vertical dims
    # reach right, then reserve that depth so the scale/paper choice + block
    # placement keep every chain -- including the OVERALL dimension -- inside the
    # frame instead of dropping the outermost level.
    top_lv, bot_lv, right_lv = estimate_dim_levels(matched, overall)
    reserves = (dim_chain_depth(top_lv) if top_lv else 0.0,
                dim_chain_depth(bot_lv) if bot_lv else 0.0,
                dim_chain_depth(right_lv) if right_lv else 0.0)
    # ASSEMBLY mode (item balloons present): balloons sit OUTSIDE every view and
    # must never touch the frame. Reserve a clearance band around the ortho block
    # = balloon diameter + leader + safety, so the placement centres the views with
    # room for the balloons on all sides (fixes balloons crossing the top frame).
    edge_clear = 0.0
    fill_max = FILL_MAX
    if balloons or bom:
        import iso_knowledge as iso
        A = iso.ISO_ASSEMBLY
        # Band reserved OUTSIDE each view for its balloons: leader + full circle
        # diameter + a breathing gap so the outermost balloon circle never reaches
        # the frame line (matches FRAME_PAD in _build_balloons). Was dia+gap+4 (=20),
        # which let a top-row balloon's rim land ON the top frame when the block was
        # pushed up; leader_len+dia+pad reserves the balloon's true vertical reach.
        edge_clear = A["balloon_leader_len"] + A["balloon_dia"] + 6.0
        # Assembly: the THREE ORTHO VIEWS are the main subject and must fill the
        # sheet. The first-angle arrangement naturally leaves the bottom-right
        # quadrant (below LEFT, right of TOP) free, which is exactly where the
        # AUXILIARY ISO and the BOM sit -- so we do NOT shrink the views with a low
        # fill cap. Keep the normal generous fill cap so the picker scales the views
        # UP to fill the available (BOM/balloon-aware) area.
        fill_max = FILL_MAX
    paper, scale, s_iso, ext, place, labels, table = _placements(
        views, buffer, n_bom, has_table, reserves, edge_clear, fill_max)
    pw, ph = PAPER[paper]
    results = {}

    scale_map = {"front": scale, "top": scale, "left": scale, "iso": s_iso}
    segs = list(_seg_iter(views, ext, place, scale_map))
    dims = _build_dimensions(matched or [], overall or [], ext, place, scale, s_iso, pw, ph)
    # Swept-path centreline overlay (+ its dims appended to `dims`).
    centerlines = _build_sweep_overlay(sweep, ext, place, scale, dims, pw, ph)
    # ASSEMBLY axes (ISO 128 centre lines for fasteners/bearings/holes): caller
    # passes axis segments in each view's model-view coords; convert to paper and
    # append as dash-dot centrelines.
    for ax in (axes or []):
        v = ax["view"]
        if v not in place:
            continue
        sc = scale_map.get(v, scale); px, py = place[v]
        x0 = px + (ax["x0"] - ext[v][0]) * sc
        y0 = py + (ax["y0"] - ext[v][1]) * sc
        x1 = px + (ax["x1"] - ext[v][0]) * sc
        y1 = py + (ax["y1"] - ext[v][1]) * sc
        centerlines.append((v, [(x0, y0), (x1, y1)]))
    # SECTION VIEW overlay: hatch the cut faces, mark the cutting line A-A on the
    # adjacent view, and retitle the sectioned view "A-A" (ISO 128-40/44/50).
    marks = _build_section_marks(section, ext, place, scale_map) if section else None
    # ASSEMBLY mode: item balloons (ISO 6433) + parts-list/BOM (ISO 7573).
    balloon_art = _build_balloons(balloons, ext, place, scale_map, pw, ph, segs, table) if balloons else None
    bom_art = _build_bom(bom, pw, ph, table) if bom else None
    # ISO 8826 bearing symbols + ISO 6410 thread lines -> paper-space line art.
    bearing_art = _build_bearings(bearings, ext, place, scale_map) if bearings else None
    thread_art = _build_threads(threads, ext, place, scale_map) if threads else None

    if "png" in fmts or "svg" in fmts:
        _render_mpl(segs, uuid, paper, scale, proj, pw, ph, out_prefix, fmts, results, labels, s_iso, dims, centerlines, marks, balloon_art, bom_art, bearing_art, thread_art, mass, title, table)
    if "dxf" in fmts:
        _render_dxf(segs, uuid, paper, scale, proj, pw, ph, out_prefix, results, labels, s_iso, dims, centerlines, marks, bearing_art, thread_art, mass, title, table)
    return paper, scale, results


def _build_bearings(bearings, ext, place, scale_map):
    """ISO 8826-1 simplified rolling-bearing symbols, projected to paper space.
    Returns dict(thick=[segs], thin=[segs]) where each seg is (x0,y0,x1,y1).
      END-ON view (axis along the sight line): OD circle (thick) + bore circle
        (thick) + a thin centre cross spanning the OD.
      SIDE view (axis in the paper plane): a thick rectangle OD x width centred on
        the bearing, a thin centreline along the axis spanning the rectangle, and
        a small thin upright cross at the centre (the conventional rolling-element
        symbol). The rectangle is built in an (along-axis u, across-axis n) frame
        so it stays square to the projected axis at any orientation."""
    import math
    thick, thin = [], []

    def to_paper(v, x, y):
        sc = scale_map.get(v, 1.0); px, py = place[v]
        return (px + (x - ext[v][0]) * sc, py + (y - ext[v][1]) * sc)

    def circle(v, cx, cy, r, bucket):
        pcx, pcy = to_paper(v, cx, cy)
        sc = scale_map.get(v, 1.0); rp = r * sc
        n = 48
        pts = [(pcx + rp * math.cos(2*math.pi*i/n), pcy + rp * math.sin(2*math.pi*i/n))
               for i in range(n + 1)]
        for i in range(n):
            bucket.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))

    for b in bearings:
        v = b["view"]
        if v not in place:
            continue
        sc = scale_map.get(v, 1.0)
        cx, cy = b["cx"], b["cy"]
        od, bore, w = b["od"], b["bore"], b["width"]
        if b.get("end_on"):
            circle(v, cx, cy, od / 2.0, thick)
            circle(v, cx, cy, bore / 2.0, thick)
            pcx, pcy = to_paper(v, cx, cy)
            rp = (od / 2.0) * sc + 2.0
            thin.append((pcx - rp, pcy, pcx + rp, pcy))
            thin.append((pcx, pcy - rp, pcx, pcy + rp))
        else:
            pcx, pcy = to_paper(v, cx, cy)
            # in-view axis unit dir; default along paper-x if degenerate
            ux, uy = b.get("ax", 1.0), b.get("ay", 0.0)
            nrm = math.hypot(ux, uy)
            if nrm < 1e-6:
                ux, uy = 1.0, 0.0
            else:
                ux, uy = ux / nrm, uy / nrm
            nx, ny = -uy, ux                       # across-axis unit
            hw = (w / 2.0) * sc                     # half width along axis
            ho = (od / 2.0) * sc                    # half OD across axis
            corners = []
            for su, so in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
                corners.append((pcx + su*hw*ux + so*ho*nx,
                                pcy + su*hw*uy + so*ho*ny))
            for i in range(4):
                a = corners[i]; bb = corners[(i+1) % 4]
                thick.append((a[0], a[1], bb[0], bb[1]))
            # thin centreline along the axis (slight overshoot)
            ov = hw + 2.0
            thin.append((pcx - ov*ux, pcy - ov*uy, pcx + ov*ux, pcy + ov*uy))
            # small conventional cross at the centre (rolling-element symbol)
            cs = min(hw, ho) * 0.5
            thin.append((pcx - cs*ux, pcy - cs*uy, pcx + cs*ux, pcy + cs*uy))
            thin.append((pcx - cs*nx, pcy - cs*ny, pcx + cs*nx, pcy + cs*ny))
    return {"thick": thick, "thin": thin}


def _build_threads(threads, ext, place, scale_map):
    """ISO 6410 conventional thread lines -> paper-space thin segments.
    SIDE entries give a minor-diameter line {x0,y0,x1,y1} in model-view coords.
    END entries {end_on,cx,cy,r} draw a 3/4 minor-dia arc (gap ~45..135 deg).
    Returns dict(thin=[segs]) (all thread linework is thin/fine per ISO 6410)."""
    import math
    thin = []

    def to_paper(v, x, y):
        sc = scale_map.get(v, 1.0); px, py = place[v]
        return (px + (x - ext[v][0]) * sc, py + (y - ext[v][1]) * sc)

    for t in threads:
        v = t["view"]
        if v not in place:
            continue
        if t.get("end_on"):
            sc = scale_map.get(v, 1.0)
            pcx, pcy = to_paper(v, t["cx"], t["cy"])
            rp = t["r"] * sc
            # 3/4 circle: open the quadrant 45..135 deg (ISO 6410 minor-dia arc)
            a0, a1 = math.radians(135), math.radians(45) + 2 * math.pi
            n = 36
            prev = None
            for i in range(n + 1):
                a = a0 + (a1 - a0) * i / n
                pt = (pcx + rp * math.cos(a), pcy + rp * math.sin(a))
                if prev is not None:
                    thin.append((prev[0], prev[1], pt[0], pt[1]))
                prev = pt
        else:
            x0, y0 = to_paper(v, t["x0"], t["y0"])
            x1, y1 = to_paper(v, t["x1"], t["y1"])
            thin.append((x0, y0, x1, y1))
    return {"thin": thin}


def _build_balloons(balloons, ext, place, scale_map, pw, ph, segs=None, table=None):
    """ISO 6433 item balloons, laid out by a GLOBAL optimiser so the number->part
    correspondence is always correct and balloons never collapse onto one point.

    Input: balloons = [{"item", "insts":[{"view","x","y"}, ...]}] -- each item with
    ALL its instance anchors projected into every ortho view (model-view coords).

    Strategy (the optimisation that fixes the systemic mis-pointing):
      1. Convert every candidate (view,instance) to a real paper-space DOT.
      2. GREEDY VIEW+INSTANCE ASSIGNMENT: place items one at a time, each choosing
         the candidate dot that is FARTHEST from all dots already placed. This
         spreads a coaxial screw/washer/nut stack across different views/instances
         instead of stacking three balloons on one collapsed point.
      3. PER-VIEW COLUMN LAYOUT: in each view, stack the circles in a right-hand
         column with a guaranteed pitch (no circle overlap), ordered by dot height
         to minimise leader crossings; the dot stays pinned to its real anchor.
    Returns dict(dots, leaders, circles, texts) in paper space."""
    import iso_knowledge as iso
    A = iso.ISO_ASSEMBLY
    R = A["balloon_dia"] / 2.0
    dots, leaders, circles, texts = [], [], [], []

    # ---- 1. candidate dots per item, in paper space, for placed views only ----
    def to_paper(c):
        v = c["view"]
        if v not in place:
            return None
        sc = scale_map.get(v, 1.0); px, py = place[v]
        return (v, px + (c["x"] - ext[v][0]) * sc, py + (c["y"] - ext[v][1]) * sc)

    items = []
    for b in balloons:
        cands = [pc for pc in (to_paper(c) for c in b.get("insts", [])) if pc]
        if cands:
            items.append({"item": b["item"], "cands": cands})

    # ---- geometry helpers (view rects, table no-go, frame limits) --------------
    # Defined BEFORE assignment because the new global assignment scores each
    # candidate by the SHORT leader it would get when routed to its nearest OPEN
    # view edge -- so it needs to know where the views, the table and the frame are.
    VIEW_PAD = R + 1.5
    view_rects = {}
    for vv in ("front", "top", "left"):
        if vv in place:
            rx0, ry0 = place[vv]
            sc_ = scale_map.get(vv, 1.0)
            view_rects[vv] = (rx0, ry0, rx0 + ext[vv][4] * sc_,
                              ry0 + ext[vv][5] * sc_)
    all_rects = list(view_rects.values())

    def _in_any_view(cx, cy):
        """True if a balloon CIRCLE centred (cx,cy) overlaps any view rect."""
        for (rx0, ry0, rx1, ry1) in all_rects:
            if (rx0 - VIEW_PAD <= cx <= rx1 + VIEW_PAD
                    and ry0 - VIEW_PAD <= cy <= ry1 + VIEW_PAD):
                return True
        return False

    tbl = None
    if table is not None:
        tdx = table.get("dx", 0.0); tdy = table.get("dy", 0.0)
        from_x = pw - MARGIN["right"] - table["tb_w"] + tdx
        top_y = MARGIN["bottom"] + table["tb_h"] + table.get("bom_reserve_h", 0.0) + tdy
        tbl = (from_x, MARGIN["bottom"] + tdy, pw - MARGIN["right"] + tdx, top_y)

    def _in_tbl(cx, cy):
        if tbl is None:
            return False
        return (tbl[0] - R <= cx <= tbl[2] + R) and (tbl[1] - R <= cy <= tbl[3] + R)

    def _seg_hits_tbl(x0, y0, x1, y1):
        if tbl is None:
            return False
        for t in range(1, 20):
            f = t / 20.0
            x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            if tbl[0] <= x <= tbl[2] and tbl[1] <= y <= tbl[3]:
                return True
        return False

    def _seg_hits_rect(x0, y0, x1, y1, rc, pad=1.0):
        # True if the segment (x0,y0)->(x1,y1) passes through rectangle rc (a view rect),
        # tested by sampling. Used to detect a balloon leader crossing another view.
        rx0, ry0, rx1, ry1 = rc[0] - pad, rc[1] - pad, rc[2] + pad, rc[3] + pad
        for t in range(0, 21):
            f = t / 20.0
            x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            if rx0 <= x <= rx1 and ry0 <= y <= ry1:
                return True
        return False

    frame_l = MARGIN["left"]; frame_r = pw - MARGIN["right"]
    frame_b = MARGIN["bottom"]; frame_t = ph - MARGIN["top"]
    # Leader stand-off from the view edge to the balloon RIM. The ISO default felt
    # cramped (balloons hugged the views), so we give a clearer visible stand-off --
    # still well within the edge_clear band (= leader_len + dia + 6) the placement
    # reserved, so the circle never reaches the frame. This is the minimum VISIBLE
    # leader the user asked for: the balloon clearly stands off, without spanning a
    # whole view.
    gap = A["balloon_leader_len"] + 5.0
    pitch = A["balloon_gap"] + 2 * R                  # centre-to-centre, no overlap
    FRAME_PAD = R + 3.0
    lim_lo_x = frame_l + R + FRAME_PAD; lim_hi_x = frame_r - R - FRAME_PAD
    lim_lo_y = frame_b + R + FRAME_PAD; lim_hi_y = frame_t - R - FRAME_PAD

    # band-occupancy test for one edge of one view, at a given coordinate along it.
    def _edge_band_blocked(v, side, coord):
        """True if the outside band of view v's `side` edge, at position `coord`
        along the edge, is covered by ANOTHER view (so routing there needs a long
        detour). Used to forbid blocked edges in first-angle stacked layouts."""
        x0, y0, x1, y1 = view_rects[v]
        if side == "top":
            cx, cy = coord, y1 + gap + R
        elif side == "bottom":
            cx, cy = coord, y0 - gap - R
        elif side == "left":
            cx, cy = x0 - gap - R, coord
        else:
            cx, cy = x1 + gap + R, coord
        for (rx0, ry0, rx1, ry1) in all_rects:
            if (rx0, ry0, rx1, ry1) == view_rects[v]:
                continue
            if (rx0 - VIEW_PAD <= cx <= rx1 + VIEW_PAD
                    and ry0 - VIEW_PAD <= cy <= ry1 + VIEW_PAD):
                return True
        return False

    # clear distance (paper mm) from one edge of view v outward to the NEAREST other
    # view (or a large number if nothing is out there). A small value means the
    # balloon would sit in a NARROW GAP between two views -- crowded, leaders from
    # both views fight over it -- so we prefer an edge that faces genuinely open space.
    def _edge_clearance(v, side):
        x0, y0, x1, y1 = view_rects[v]
        best = 1e6
        for (rx0, ry0, rx1, ry1) in all_rects:
            if (rx0, ry0, rx1, ry1) == view_rects[v]:
                continue
            if side == "top" and ry0 >= y1 and not (rx1 < x0 or rx0 > x1):
                best = min(best, ry0 - y1)
            elif side == "bottom" and ry1 <= y0 and not (rx1 < x0 or rx0 > x1):
                best = min(best, y0 - ry1)
            elif side == "left" and rx1 <= x0 and not (ry1 < y0 or ry0 > y1):
                best = min(best, x0 - rx1)
            elif side == "right" and rx0 >= x1 and not (ry1 < y0 or ry0 > y1):
                best = min(best, rx0 - x1)
        return best

    NEED = 2.0 * (gap + 2 * R)                         # clear space a balloon wants

    def _best_edge(v, fx, fy):
        """Pick the edge of view v giving the SHORTEST honest leader for dot (fx,fy):
        the nearest edge whose outside band (at the dot's own coordinate) is OPEN and
        faces genuinely clear space. Blocked edges get a big penalty; edges facing a
        NARROW GAP between this and a neighbour view get a soft penalty so a balloon
        prefers the open side. Returns (side, leader_len)."""
        x0, y0, x1, y1 = view_rects[v]
        cand = {"left": fx - x0, "right": x1 - fx,
                "bottom": fy - y0, "top": y1 - fy}
        scored = {}
        for s_, dist in cand.items():
            # Would-be balloon centre just outside this edge (at the dot's coordinate).
            if s_ == "left":
                bcx, bcy = x0 - gap - R, fy
            elif s_ == "right":
                bcx, bcy = x1 + gap + R, fy
            elif s_ == "bottom":
                bcx, bcy = fx, y0 - gap - R
            else:                                    # top
                bcx, bcy = fx, y1 + gap + R
            # If the frame would clamp that centre back INTO the printable band (i.e.
            # this view edge sits too close to the frame to route the balloon clear),
            # the edge is un-routable: the balloon would be dumped onto the view. Reject
            # it hard so a genuinely open edge (with room) is chosen instead. This fixes
            # balloons that landed ON a part at a view edge near the sheet frame.
            clamped = (bcx < lim_lo_x or bcx > lim_hi_x or
                       bcy < lim_lo_y or bcy > lim_hi_y)
            if _edge_band_blocked(v, s_, fx if s_ in ("top", "bottom") else fy) or clamped:
                pen = 1e6
            else:
                clr = _edge_clearance(v, s_)
                pen = max(0.0, NEED - clr) * 0.6      # soft: narrow gap -> mild push
                # OTHER-VIEW CROSSING penalty: the leader runs from the anchor (fx,fy)
                # to the balloon centre (bcx,bcy) just outside this edge. If that segment
                # passes through ANOTHER view's rectangle, the leader visibly crosses that
                # view (e.g. an anchor at the centre of the TOP disc routed UP crosses into
                # the FRONT view). Penalise it hard so the balloon prefers an edge whose
                # leader exits into open space (for a disc-centre anchor, the LEFT/RIGHT
                # edges lead out sideways to empty margin, the TOP/BOTTOM edges into the
                # stacked views). This realises "route 1 and 3 to the sides, not across TOP".
                for _ov, _rc in view_rects.items():
                    if _ov == v:
                        continue
                    if _seg_hits_rect(fx, fy, bcx, bcy, _rc):
                        pen += 500.0
                        break
            scored[s_] = dist + pen
        side = min(scored, key=lambda k: scored[k])
        return side, cand[side]

    # ---- 2. GLOBAL ASSIGNMENT: one (view,instance) candidate per item ----------
    # For every candidate we compute the SHORT leader it would receive when routed
    # to its nearest OPEN view edge, then pick the assignment minimising a holistic
    # cost expressed entirely in PAPER MILLIMETRES so the terms are commensurable:
    #   leader   -- mm of honest leader to the nearest open edge (dominant; req 3)
    #   crowd    -- mm this balloon will be SHOVED along the edge by the de-overlap
    #               because other balloons already cluster at the same edge/coord;
    #               this lets a coaxial stack place a couple of balloons in a tidy
    #               row but pushes the 3rd/4th member to another view/side instead
    #               of piling onto one point (reqs 5 & 6)
    #   exposure -- small bias (~one pitch) toward dots on the silhouette over ones
    #               buried in the view interior (a coaxial stack hidden behind a part)
    #   side     -- small bias toward FRONT/LEFT, which carry the readable profiles
    SIDE_VIEWS = ("front", "left")

    def _vbbox(v):
        return view_rects.get(v)

    def _exposure(v, fx, fy):
        bb = _vbbox(v)
        if bb is None:
            return 1.0
        x0, y0, x1, y1 = bb
        hw = max((x1 - x0) / 2.0, 1e-6); hh = max((y1 - y0) / 2.0, 1e-6)
        dx = min(fx - x0, x1 - fx) / hw
        dy = min(fy - y0, y1 - fy) / hh
        return max(0.0, min(1.0, min(dx, dy)))

    # de-duplicate identical candidates (multi-instance items repeat them) so the
    # collision logic sees distinct positions, not the same point many times.
    for it in items:
        seen = set(); uniq = []
        for (v, fx, fy) in it["cands"]:
            k = (v, round(fx, 1), round(fy, 1))
            if k not in seen:
                seen.add(k); uniq.append((v, fx, fy))
        it["cands"] = uniq

    # The number used along an edge: balloons sharing an edge are fanned out by the
    # layout with this centre-to-centre PITCH, so the k-th balloon clustered at one
    # coordinate ends up ~k*pitch from its feature. We model that displacement as the
    # crowding cost, which is exactly the leader degradation it causes.
    def _along(side, fx, fy):
        return fx if side in ("top", "bottom") else fy

    # Two dots closer than this (paper mm) read as POINTING AT THE SAME PART -- the
    # core "many balloons -> one fastener" bug. A coaxial screw head + washer + nut
    # collapse to one point in the AXIAL view but separate vertically in the SIDE
    # view; this radius drives the picker to the side view where they are distinct.
    SAMESPOT = max(pitch, 3.0 * R)

    def _cand_cost(v, fx, fy, placed):
        """Cost (lower=better) of giving this item the candidate dot (v,fx,fy).

        Three forces, all in paper mm:
          DISTINCTNESS (dominant) -- a dot landing near ANOTHER item's chosen dot
            means two balloons point at the SAME visible spot (a coaxial stack seen
            end-on). Heavily penalised so screw/washer/nut migrate to the SIDE view
            where the head sits high, the washer just below, the nut lowest -- three
            DISTINCT points on one axis (the intuitive ISO way the user asked for).
          LEADER -- short honest leaders beside the feature (req 3).
          READABILITY -- small bias toward silhouette dots and the FRONT/LEFT
            profile views that carry the readable fastener heads/nuts."""
        side, lead = _best_edge(v, fx, fy)
        c = lead                                     # mm of honest leader
        # CROSSING penalty: estimate the balloon centre just outside the chosen edge and
        # penalise HARD if the straight leader from the anchor to it would cross ANOTHER
        # view. This steers the optimiser to the view/side where the fastener anchor is
        # near an OPEN edge (a short leader into empty margin) instead of one buried in a
        # view whose leader must span the stacked views (the "leader across TOP" case).
        x0, y0, x1, y1 = view_rects[v]
        if side == "left":
            bcx, bcy = x0 - gap - R, fy
        elif side == "right":
            bcx, bcy = x1 + gap + R, fy
        elif side == "bottom":
            bcx, bcy = fx, y0 - gap - R
        else:
            bcx, bcy = fx, y1 + gap + R
        for _ov, _rc in view_rects.items():
            if _ov != v and _seg_hits_rect(fx, fy, bcx, bcy, _rc, pad=-2.0):
                c += 200.0
                break
        # distinctness: distance to the NEAREST already-placed dot. Closer => worse.
        for (pi, pv, pfx, pfy, pside) in placed:
            d = ((fx - pfx) ** 2 + (fy - pfy) ** 2) ** 0.5
            if d < SAMESPOT:
                # ramp that is CATASTROPHIC at near-exact coincidence (two balloons
                # on one spot = the core bug) but cheap at a near-miss, so an item
                # would rather sit a pitch away from a neighbour than dead on it.
                near = 1.0 - d / SAMESPOT             # 0..1
                c += 45.0 * near * near
                if d < 1.2 * R:                       # essentially the SAME point
                    c += 120.0
        c += _exposure(v, fx, fy) * 10.0             # silhouette bias
        if v not in SIDE_VIEWS:
            c += 6.0                                  # bias toward FRONT/LEFT profiles
        return c, side

    def _total_cost(plc):
        tot = 0.0
        for k in range(len(plc)):
            it_, v, fx, fy, side = plc[k]
            others = plc[:k] + plc[k + 1:]
            cst, _s = _cand_cost(v, fx, fy, others)
            tot += cst
        return tot

    def _greedy(order):
        plc = []
        for it in order:
            best = None
            for (v, fx, fy) in it["cands"]:
                cost, side = _cand_cost(v, fx, fy, plc)
                if best is None or cost < best[0]:
                    best = (cost, v, fx, fy, side)
            _, v, fx, fy, side = best
            plc.append((it["item"], v, fx, fy, side))
        return plc

    # Greedy global assignment with a few orderings + the repair sweep below; keep
    # the lowest-total-cost result (local search with restarts breaks the ties that
    # leave two distinct fasteners stacked on one spot in an over-constrained part).
    import random as _random
    base = sorted(items, key=lambda d: (len(d["cands"]), d["item"]))
    orderings = [base, list(reversed(base)),
                 sorted(items, key=lambda d: -len(d["cands"]))]
    rng = _random.Random(12345)
    for _ in range(5):
        shuf = list(items); rng.shuffle(shuf); orderings.append(shuf)
    placed = None; placed_cost = None
    for od in orderings:
        cand_plc = _greedy(od)
        cc = _total_cost(cand_plc)
        if placed is None or cc < placed_cost:
            placed, placed_cost = cand_plc, cc

    # Repair pass: re-pick each item against ALL OTHERS (it was chosen before some
    # of them existed) to relax residual collisions -- a few sweeps converge.
    for _sweep in range(8):
        changed = False
        for i in range(len(placed)):
            it = next(d for d in items if d["item"] == placed[i][0])
            others = placed[:i] + placed[i + 1:]
            best = None
            for (v, fx, fy) in it["cands"]:
                cost, side = _cand_cost(v, fx, fy, others)
                if best is None or cost < best[0]:
                    best = (cost, v, fx, fy, side)
            _, v, fx, fy, side = best
            if (v, fx, fy, side) != tuple(placed[i][1:]):
                placed[i] = (placed[i][0], v, fx, fy, side)
                changed = True
        if not changed:
            break

    # drop the routed side back out; keep (item, view, fx, fy) for the layout step
    placed = [(item, v, fx, fy) for (item, v, fx, fy, side) in placed]

    # ---- 3. per-view EDGE layout (balloons OUTSIDE each view, no crossings) -----
    # Each feature dot is tagged to the NEAREST view edge (top/bottom/left/right);
    # its balloon is placed just OUTSIDE that edge. Balloons on the same edge are
    # ordered by the feature's position ALONG the edge, so leaders run radially
    # outward and never cross (crossings only happen when balloon order disagrees
    # with feature order). The leader is a short straight line from the real dot to
    # the balloon's near rim, so it does not cut back across the view interior or
    # through other holes. The BOM/title-block rectangle is a no-go zone for both
    # circles and leaders.
    by_view = {}
    for (item, v, fx, fy) in placed:
        by_view.setdefault(v, []).append((item, fx, fy))

    for v, group in by_view.items():
        sc = scale_map.get(v, 1.0); px, py = place[v]
        vx0 = px; vx1 = px + ext[v][4] * sc          # view L/R edges (paper)
        vy0 = py; vy1 = py + ext[v][5] * sc          # view B/T edges (paper)
        vcx = (vx0 + vx1) / 2.0; vcy = (vy0 + vy1) / 2.0

        # Helper: is a given edge of THIS view open (outside band not covered by a
        # neighbour view) for a dot at coordinate (fx,fy)?
        def _edge_open(side_, fx, fy):
            return not _edge_band_blocked(
                v, side_, fx if side_ in ("top", "bottom") else fy)

        # Tag each dot to an edge. Start from the NEAREST OPEN edge (short leader),
        # then SPLIT COAXIAL STACKS: several fasteners on one axis (a screw head +
        # washer + nut) project to the SAME along-axis coordinate in a side view but
        # at DIFFERENT heights. If they all routed to the same (nearest) edge their
        # leaders would cross and pile up. Instead we send the UPPER members to the
        # TOP edge and the LOWER members to the BOTTOM edge (or LEFT/RIGHT for a
        # horizontal axis), so each balloon points cleanly at its own member -- the
        # intuitive ISO side-view callout. Only OPEN edges are used.
        prelim = []
        for (item, fx, fy) in group:
            side, _lead = _best_edge(v, fx, fy)
            prelim.append([item, fx, fy, side])

        # Detect a COAXIAL stack and split it across the TOP and BOTTOM edges. A
        # screw head + washer + nut on one (vertical) axis project to the SAME x in
        # a side view but to DIFFERENT y (head high, nut low). We cluster dots that
        # share an x (the axis) and, when such a cluster genuinely separates in y but
        # by no more than a compact stack height, route its UPPER members to the TOP
        # edge and LOWER members to the BOTTOM edge so each balloon points cleanly at
        # its own member. We deliberately do NOT cluster by shared y: several
        # DIFFERENT bolts sit at the SAME height (same y, different x) and must each
        # keep its own nearest edge -- they are not one stack.
        AXTOL = 1.6 * R                               # max x-spread within a stack
        STACKMAX = 5.0 * pitch                        # max y-spread of a real stack
        used = [False] * len(prelim)
        for i in range(len(prelim)):
            if used[i]:
                continue
            xi = prelim[i][1]
            grp = [k for k in range(len(prelim))
                   if not used[k] and abs(prelim[k][1] - xi) <= AXTOL]
            if len(grp) < 2:
                continue
            ys = [prelim[k][2] for k in grp]
            yspan = max(ys) - min(ys)
            yi = sum(ys) / len(ys)
            if not (R < yspan <= STACKMAX):
                continue                              # not a compact coaxial stack
            if not (_edge_open("top", xi, yi) and _edge_open("bottom", xi, yi)):
                continue                              # need both edges to split into
            grp.sort(key=lambda k: prelim[k][2])      # by y, low..high
            mid = len(grp) // 2
            for r, k in enumerate(grp):
                prelim[k][3] = "bottom" if r < mid else "top"
                used[k] = True

        sided = {"top": [], "bottom": [], "left": [], "right": []}
        for (item, fx, fy, side) in prelim:
            sided[side].append((item, fx, fy))

        # Lay out each side's balloons just outside that edge, at the feature's own
        # coordinate (short leader), de-overlapped along the edge. The leader length
        # is the small gap from the edge to the balloon -- never spanning the view.
        for side, members in sided.items():
            if not members:
                continue
            n = len(members)
            if side in ("left", "right"):
                members = sorted(members, key=lambda m: m[2])   # by feature y
                cx = (vx1 + gap + R) if side == "right" else (vx0 - gap - R)
                sdir = 1.0 if side == "right" else -1.0
                for _ in range(40):
                    if not any(_in_any_view(cx, vcy + (k - (n-1)/2.0) * pitch)
                               for k in range(n)):
                        break
                    cx += sdir * (R + 2.0)
                cx = min(max(cx, lim_lo_x), lim_hi_x)
                # each balloon at its OWN feature y; de-overlap CENTRED on the group
                # so the spread is symmetric (not all pushed one way) -> leaders stay
                # short on both ends and ordered = no crossings.
                ys = [min(max(fy, lim_lo_y), lim_hi_y) for (_it, _fx, fy) in members]
                for i in range(1, len(ys)):
                    if ys[i] - ys[i-1] < pitch:
                        ys[i] = ys[i-1] + pitch
                overflow = (ys[-1] - ys[0]) - (members[-1][2] - members[0][2]) \
                    if n > 1 else 0.0
                if overflow > 0:                      # re-centre the spread block
                    ctr = sum(m[2] for m in members) / n
                    half = (ys[-1] - ys[0]) / 2.0
                    base = ctr - half
                    ys = [base + i * 0 + (ys[i] - ys[0]) for i in range(n)]
                ys = [min(max(y, lim_lo_y), lim_hi_y) for y in ys]
                for i, (item, fx, fy) in enumerate(members):
                    cy = ys[i]
                    guard = 0
                    while (_in_tbl(cx, cy) or _seg_hits_tbl(fx, fy, cx, cy)
                           or _in_any_view(cx, cy)) and guard < 30:
                        guard += 1
                        if _in_any_view(cx, cy):
                            nxt = cx + sdir * (R + 2.0)
                            nxt = min(max(nxt, lim_lo_x), lim_hi_x)
                            # if the frame clamp would put the circle back ON the view,
                            # the edge is unusable: stop rather than oscillate in place.
                            if _in_any_view(nxt, cy):
                                break
                            cx = nxt
                        else:
                            cy += pitch
                            if cy > lim_hi_y:
                                break
                    rim = (cx - R, cy) if side == "right" else (cx + R, cy)
                    dots.append((fx, fy, A["balloon_dot_r"]))
                    leaders.append((fx, fy, rim[0], rim[1]))
                    circles.append((cx, cy, R))
                    texts.append((cx, cy, str(item)))
            else:  # top / bottom -> horizontal row
                members = sorted(members, key=lambda m: m[1])   # by feature x
                cy = (vy1 + gap + R) if side == "top" else (vy0 - gap - R)
                sdir = 1.0 if side == "top" else -1.0
                for _ in range(40):
                    if not any(_in_any_view(vcx + (k - (n-1)/2.0) * pitch, cy)
                               for k in range(n)):
                        break
                    cy += sdir * (R + 2.0)
                cy = min(max(cy, lim_lo_y), lim_hi_y)
                # each balloon at its OWN feature x; de-overlap, then re-centre the
                # spread block on the features' centroid so it stays beside them.
                xs = [min(max(fx, lim_lo_x), lim_hi_x) for (_it, fx, _fy) in members]
                for i in range(1, len(xs)):
                    if xs[i] - xs[i-1] < pitch:
                        xs[i] = xs[i-1] + pitch
                if n > 1 and (xs[-1] - xs[0]) > (members[-1][1] - members[0][1]):
                    ctr = sum(m[1] for m in members) / n
                    half = (xs[-1] - xs[0]) / 2.0
                    base = ctr - half
                    xs = [base + (xs[i] - xs[0]) for i in range(n)]
                xs = [min(max(x, lim_lo_x), lim_hi_x) for x in xs]
                for i, (item, fx, fy) in enumerate(members):
                    cx = xs[i]
                    guard = 0
                    while (_in_tbl(cx, cy) or _seg_hits_tbl(fx, fy, cx, cy)
                           or _in_any_view(cx, cy)) and guard < 30:
                        guard += 1
                        if _in_any_view(cx, cy):
                            cy += sdir * (R + 2.0)
                            cy = min(max(cy, lim_lo_y), lim_hi_y)
                        else:
                            cx -= pitch
                            if cx < lim_lo_x:
                                break
                    rim = (cx, cy - R) if side == "top" else (cx, cy + R)
                    dots.append((fx, fy, A["balloon_dot_r"]))
                    leaders.append((fx, fy, rim[0], rim[1]))
                    circles.append((cx, cy, R))
                    texts.append((cx, cy, str(item)))

    # ---- 4. GLOBAL de-overlap + leader cleanup ---------------------------------
    # The per-edge layout cannot see balloons from a DIFFERENT view/edge that land
    # in the same clear band (e.g. a FRONT right-edge balloon and a LEFT left-edge
    # balloon meeting in the narrow gap between the two views). Relax all circle
    # centres against each other so no two circles overlap, keeping each clear of
    # the views/table/frame, then re-aim every leader at the NEAREST point on its
    # balloon rim (honest short leader attached on the side facing the feature).
    cen = [[cx, cy] for (cx, cy, _r) in circles]
    feat = [(lx0, ly0) for (lx0, ly0, _x1, _y1) in leaders]   # anchor dots
    minsep = pitch
    for _it in range(60):
        moved = False
        for i in range(len(cen)):
            for j in range(i + 1, len(cen)):
                dx = cen[j][0] - cen[i][0]; dy = cen[j][1] - cen[i][1]
                d = (dx * dx + dy * dy) ** 0.5
                if d >= minsep:
                    continue
                if d < 1e-6:
                    dx, dy, d = 1.0, 0.0, 1.0
                push = (minsep - d) / 2.0 + 0.1
                ux, uy = dx / d, dy / d
                # move each circle away from the other, but only along the axis that
                # keeps it OUTSIDE the views; clamp into the frame and off the table.
                for (k, sgn) in ((i, -1.0), (j, +1.0)):
                    nx = cen[k][0] + sgn * ux * push
                    ny = cen[k][1] + sgn * uy * push
                    nx = min(max(nx, lim_lo_x), lim_hi_x)
                    ny = min(max(ny, lim_lo_y), lim_hi_y)
                    if _in_any_view(nx, ny) or _in_tbl(nx, ny):
                        # blocked: try shifting purely tangentially instead
                        nx2 = cen[k][0] - sgn * uy * push
                        ny2 = cen[k][1] + sgn * ux * push
                        nx2 = min(max(nx2, lim_lo_x), lim_hi_x)
                        ny2 = min(max(ny2, lim_lo_y), lim_hi_y)
                        if not (_in_any_view(nx2, ny2) or _in_tbl(nx2, ny2)):
                            nx, ny = nx2, ny2
                        else:
                            continue
                    cen[k][0], cen[k][1] = nx, ny
                    moved = True
        if not moved:
            break
    for idx in range(len(circles)):
        cx, cy, r = circles[idx]
        ncx, ncy = cen[idx]
        circles[idx] = (ncx, ncy, r)
        t = texts[idx]
        texts[idx] = (ncx, ncy, t[2])
        fxx, fyy = feat[idx]
        vx = ncx - fxx; vy = ncy - fyy
        vlen = (vx * vx + vy * vy) ** 0.5 or 1.0
        rimx = ncx - (vx / vlen) * r; rimy = ncy - (vy / vlen) * r
        leaders[idx] = (fxx, fyy, rimx, rimy)

    # FINAL LEADER-CROSSING FIX (short leader): after placement, some balloons end up
    # with a long leader that crosses a view (a fastener/body anchored inside a view,
    # whose balloon was pushed all the way to a frame edge, the leader spanning the
    # stacked views). Rather than force it to a distant edge, place the balloon in the
    # NEAREST open spot around the anchor with a SHORT leader: search outward in small
    # rings and many directions for the closest position where (a) the balloon circle
    # clears every view, the table and other balloons, and (b) the short leader from the
    # anchor to it does not cross a view. This is the user's point -- keep the leader
    # short and drop the balloon into the nearest gap, instead of routing it across the
    # sheet.
    def _leader_crosses_any(ax, ay, bx, by):
        for _v, _rc in view_rects.items():
            if _seg_hits_rect(ax, ay, bx, by, _rc, pad=-2.0):
                return True
        return False

    def _spot_clear(bx, by):
        # balloon circle at (bx,by) must be inside the frame and clear of all views/table
        if not (frame_l + R <= bx <= frame_r - R and frame_b + R <= by <= frame_t - R):
            return False
        for _rc in view_rects.values():
            if _rc[0] - R <= bx <= _rc[2] + R and _rc[1] - R <= by <= _rc[3] + R:
                return False
        if tbl is not None and tbl[0] - R <= bx <= tbl[2] + R and tbl[1] - R <= by <= tbl[3] + R:
            return False
        return True

    def _circle_on_view(bx, by):
        # balloon circle centre sits on a view (its centre is inside a view rect, so the
        # circle overlaps the linework -- not merely standing just outside an edge).
        for _rc in view_rects.values():
            if _rc[0] <= bx <= _rc[2] and _rc[1] <= by <= _rc[3]:
                return True
        return False

    import math as _mm
    occupied = [(_c[0], _c[1]) for _c in circles]
    for idx in range(len(circles)):
        cx, cy, r = circles[idx]
        fxx, fyy = feat[idx]
        ax0, ay0, bx0, by0 = leaders[idx]
        # relocate when the leader crosses a view OR the balloon sits ON a view.
        if not (_leader_crosses_any(ax0, ay0, bx0, by0) or _circle_on_view(cx, cy)):
            continue
        # spiral out from the anchor: nearest clear spot with a short, non-crossing leader
        best = None
        rad = gap + R                                # start one stand-off out
        while rad <= 120.0 and best is None:
            for k in range(24):                      # 24 directions per ring
                ang = 2.0 * _mm.pi * k / 24.0
                bxc = fxx + rad * _mm.cos(ang)
                byc = fyy + rad * _mm.sin(ang)
                if not _spot_clear(bxc, byc):
                    continue
                # short leader from anchor to the near rim of this balloon
                dx = bxc - fxx; dy = byc - fyy
                dl = (dx * dx + dy * dy) ** 0.5 or 1.0
                rimx2 = bxc - dx / dl * r; rimy2 = byc - dy / dl * r
                if _leader_crosses_any(fxx, fyy, rimx2, rimy2):
                    continue
                clash = any(abs(bxc - ox) < 2 * R and abs(byc - oy) < 2 * R
                            for (ox, oy) in occupied if (ox, oy) != (cx, cy))
                cost = rad + (1e4 if clash else 0.0)
                if best is None or cost < best[0]:
                    best = (cost, bxc, byc, rimx2, rimy2)
            rad += 6.0
        if best is not None:
            _, bxc, byc, rimx2, rimy2 = best
            circles[idx] = (bxc, byc, r)
            texts[idx] = (bxc, byc, texts[idx][2])
            leaders[idx] = (fxx, fyy, rimx2, rimy2)
            occupied[idx] = (bxc, byc)
    return {"dots": dots, "leaders": leaders, "circles": circles, "texts": texts}


# ISO 7573 BOM columns (drawing-layer definition so the layout owns the table).
# Relative widths sum need not match -- they are scaled to the (adaptive) table_w.
# Columns: No. | Qty | Designation | Reference | Material | Weight
BOM_COLS = [9.0, 9.0, 50.0, 40.0, 26.0, 24.0]
BOM_HEADERS = ["No.", "Qty", "Designation", "Reference", "Material", "Weight"]
# Per-column horizontal alignment of VALUES (and headers): the narrow numeric
# columns (No., Qty) are CENTRED; the wider text columns stay LEFT-aligned.
BOM_ALIGN = ["center", "center", "left", "left", "left", "left"]


def _build_bom(bom, pw, ph, table):
    """ISO 7573 parts list directly ABOVE the title block: header row + one row per
    item, item 1 at the bottom (numbering upward). The table is the SAME WIDTH and
    LEFT EDGE as the (adaptive) title block. `table` carries tb_w / row_h. The
    Material and Weight value cells are LEFT BLANK on purpose (generated dataset --
    material/mass are not asserted); the column HEADERS are still shown.
    Returns dict(lines, texts) where each text is (x, y, t, hdr, ha, size)."""
    table_w = table["tb_w"]
    rh = table["row_h"]
    tb_h = table["tb_h"]
    fac = table_w / sum(BOM_COLS)
    cols = [w * fac for w in BOM_COLS]              # scaled to fill table_w
    # group-centering shift (see _placements): the BOM moves with the views/title.
    x0 = pw - MARGIN["right"] - table_w + table.get("dx", 0.0)  # title-block left edge
    y0 = MARGIN["bottom"] + tb_h + table.get("dy", 0.0)         # on title block
    rows = list(bom)
    rows = list(reversed(rows))                     # draw bottom-up; item1 lowest
    nrow = len(rows) + 1                            # +1 header
    lines, texts = [], []
    # text/header font sizes scale with the (adaptive) row height (mpl pt ~= mm/0.353)
    vsize = max(4.5, min(8.0, rh * 0.95))
    hsize = vsize + 0.6
    pad = max(1.2, rh * 0.18)
    # outer + row grid
    for r in range(nrow + 1):
        y = y0 + r * rh
        lines.append((x0, y, x0 + table_w, y))
    cx = x0
    for w in cols + [0]:
        lines.append((cx, y0, cx, y0 + nrow * rh))
        cx += w

    def cell_x(left, w, ha):
        return (left + w / 2.0) if ha == "center" else (left + pad)

    # header (top row): ALL column titles are CENTRED in their cells.
    hy = y0 + (nrow - 0.5) * rh
    cx = x0
    for h, w in zip(BOM_HEADERS, cols):
        texts.append((cell_x(cx, w, "center"), hy, h, True, "center", hsize))
        cx += w
    # data rows bottom-up. Material + Weight values are intentionally BLANK.
    for ri, row in enumerate(rows):
        ry = y0 + (ri + 0.5) * rh
        vals = [str(row.get("item", "")), str(row.get("qty", "")),
                row.get("designation", ""), row.get("reference", ""),
                "",                                   # Material -> blank
                ""]                                   # Weight   -> blank
        cx = x0
        for val, w, ha in zip(vals, cols, BOM_ALIGN):
            if val:
                texts.append((cell_x(cx, w, ha), ry, val, False, ha, vsize))
            cx += w
    return {"lines": lines, "texts": texts}


# Which view carries the CUTTING LINE for a section in <key>, and the viewing
# direction's image in that adjacent view's local coords. The cutting plane
# passes through the model origin: a horizontal line (local y=0) when the plane
# is edge-on horizontally there, vertical (local x=0) otherwise.
_SECTION_ADJ = {
    # adj view, line axis there, sight-arrow dir, sign mapping the cutting-plane
    # offset (model coord along the view dir) into the adj view's LOCAL coords
    # (top local y = -y_model, hence -1 for front sections).
    "front": ("top",   "y", (0, 1), -1.0),   # plane y=off; dir -Y -> top +y
    "left":  ("front", "x", (1, 0), +1.0),   # plane x=off; dir +X -> front +x
    "top":   ("front", "y", (0, -1), +1.0),  # plane z=off; dir -Z -> front -y
}


def _build_section_marks(section, ext, place, scale_map):
    """Paper-space artwork for a section view: 45-deg hatch segments over the cut
    faces, thick end strokes + sight-direction arrows + 'A' letters on the
    adjacent view's cutting line, and the 'A-A' label override."""
    import projlib
    vn = section["view"]
    sc = scale_map[vn]; ox, oy = place[vn]
    hatch = []
    for face in section.get("faces", []):
        # transform the cut-face boundary to PAPER space first, then hatch there
        # so the 45-deg line spacing is a true 2.5 mm on paper at any view scale.
        fp = [(ox + (x0 - ext[vn][0]) * sc, oy + (y0 - ext[vn][1]) * sc,
               ox + (x1 - ext[vn][0]) * sc, oy + (y1 - ext[vn][1]) * sc)
              for (x0, y0, x1, y1) in face]
        hatch.extend(projlib.hatch_segments(fp, spacing=2.5))
    adj, axis, adir, osign = _SECTION_ADJ[vn]
    cpos = osign * section.get("offset", 0.0)   # cutting line, adj-local coords
    sa = scale_map[adj]; ax0, ay0 = place[adj]
    minx, miny, w, h = ext[adj][0], ext[adj][1], ext[adj][4], ext[adj][5]
    strokes, arrows, texts = [], [], []
    S = 5.0      # end-stroke length (mm paper)
    if axis == "y":
        ypl = ay0 + (cpos - miny) * sa
        xa = ax0 - 2.0; xb = ax0 + w * sa + 2.0
        strokes = [(xa - S, ypl, xa, ypl), (xb, ypl, xb + S, ypl)]
        arrows = [(xa - S / 2, ypl, adir[0], adir[1]),
                  (xb + S / 2, ypl, adir[0], adir[1])]
        texts = [(xa - S - 2.5, ypl, "A"), (xb + S + 2.5, ypl, "A")]
    else:
        xpl = ax0 + (cpos - minx) * sa
        ya = ay0 - 2.0; yb = ay0 + h * sa + 2.0
        strokes = [(xpl, ya - S, xpl, ya), (xpl, yb, xpl, yb + S)]
        arrows = [(xpl, ya - S / 2, adir[0], adir[1]),
                  (xpl, yb + S / 2, adir[0], adir[1])]
        texts = [(xpl, ya - S - 2.5, "A"), (xpl, yb + S + 2.5, "A")]
    return {"hatch": hatch, "strokes": strokes, "arrows": arrows,
            "texts": texts, "label_view": vn}


def _frame_lines(pw, ph, table=None):
    """Border + title block outer rectangle lines as list of (x0,y0,x1,y1).
    `table` (from _placements) gives the ADAPTIVE title-block w/h; falls back to the
    module target if absent."""
    bl, bb = MARGIN["left"], MARGIN["bottom"]
    br, bt = pw - MARGIN["right"], ph - MARGIN["top"]
    tb_w = table["tb_w"] if table else TITLEBLOCK_W
    tb_h = table["tb_h"] if table else TITLEBLOCK_H
    lines = [
        (bl, bb, br, bb), (br, bb, br, bt), (br, bt, bl, bt), (bl, bt, bl, bb),
    ]
    # group-centering shift (see _placements): the title block moves with the views
    # so the WHOLE content block is centred and the four margins stay balanced. The
    # outer FRAME above is fixed at the page margins; only the title-block box moves.
    tdx = table.get("dx", 0.0) if table else 0.0
    tdy = table.get("dy", 0.0) if table else 0.0
    # title block outer box (full rectangle; when shifted it no longer reuses the
    # frame border, so draw all four sides).
    tbx = br - tb_w + tdx
    tbx1 = br + tdx
    tby0 = bb + tdy
    tby = bb + tb_h + tdy
    lines += [
        (tbx, tby0, tbx, tby), (tbx, tby, tbx1, tby),       # left, top
        (tbx1, tby0, tbx1, tby), (tbx, tby0, tbx1, tby0),   # right, bottom
    ]
    return lines, (tbx, tby0, tbx1, tby)


def _fit_title(T, title, cx, cy, cell_w, max_size=7.0, min_size=3.6):
    """Emit the (possibly long) Title into the Title cell centred at (cx, cy),
    shrinking the font and, if still too long, wrapping onto two lines so a full
    identifier (e.g. '0a81a0b7-2d9a-...__M4_socket__asm') fits without overrunning
    the cell. Uses a coarse char-width estimate (~0.55*size mm per glyph)."""
    def width(s, sz):
        return 0.55 * sz * len(s)
    # 1) single line, shrink to fit
    sz = max_size
    while sz > min_size and width(title, sz) > cell_w:
        sz -= 0.3
    if width(title, sz) <= cell_w:
        T(cx, cy, title, sz, ha="center", bold=True)
        return
    # 2) two lines: split near the middle, preferably at a separator
    n = len(title)
    seps = [i for i, c in enumerate(title) if c in "-_ "]
    mid = min(seps, key=lambda i: abs(i - n // 2)) if seps else n // 2
    l1, l2 = title[:mid + 1].rstrip("-_ "), title[mid + 1:].lstrip("-_ ")
    sz = max_size - 1.0
    while sz > min_size and (width(l1, sz) > cell_w or width(l2, sz) > cell_w):
        sz -= 0.3
    T(cx, cy + 0.6 * sz, l1, sz, ha="center", bold=True)
    T(cx, cy - 0.6 * sz, l2, sz, ha="center", bold=True)


def _titleblock(pw, ph, uuid, paper, scale, s_iso=None, title=None,
                material=None, mass=None, first_angle=True, table=None):
    """ISO 7200 title strip (bottom-right), sized to the ADAPTIVE table dims in
    `table` (~2x the old compact strip, scaled down on a tight sheet). Two rows:
      LEFT  description zone : Drawn | Checked | Date row (blank fill-in cells) over
                               a Title row (the full identifier).
      RIGHT meta zone        : a CENTRED projection-symbol + "ISO 5456-2 / 1st angle"
                               cell (top) over a Scale | Sheet | Drawing No row.
    Empty data cells (Drawn/Checked/Date) are left BLANK for hand entry. Returns
    (lines, texts[(x,y,txt,size,ha,va,bold)], psym_at(cx,cy,r))."""
    tb_w = table["tb_w"] if table else TITLEBLOCK_W
    tb_h = table["tb_h"] if table else TITLEBLOCK_H
    # group-centering shift (see _placements): title strip moves with the content.
    br = pw - MARGIN["right"] + (table.get("dx", 0.0) if table else 0.0)
    bb = MARGIN["bottom"] + (table.get("dy", 0.0) if table else 0.0)
    x0 = br - tb_w
    y0 = bb
    W, H = tb_w, tb_h
    x1 = br
    y1 = y0 + H

    lines = []
    texts = []
    # Font sizes scale with the (now larger) strip height so the text is legible but
    # never overflows. CAP = field caption, V = value.
    CAP = max(3.2, min(6.0, H * 0.115))
    V = CAP + 1.1
    pad = max(1.2, H * 0.045)
    cap_in = max(0.8, H * 0.03)             # caption inset from the cell top
    def T(x, y, t, size=CAP, ha="left", va="center", bold=False):
        texts.append((x, y, t, size, ha, va, bold))

    # description | meta vertical split (left ~58%, right meta ~42%).
    meta_w = 0.42 * W
    xm = x1 - meta_w
    lines.append((xm, y0, xm, y1))

    # one horizontal mid-rule splitting each zone into an upper and lower row.
    y_mid = y0 + 0.5 * H

    # --- LEFT (description) zone -------------------------------------------
    L_x = x0
    lines.append((L_x, y_mid, xm, y_mid))
    desc_w = xm - L_x
    name_x = L_x + 0.34 * desc_w
    date_x = xm - 0.30 * desc_w
    lines.append((name_x, y_mid, name_x, y1))
    lines.append((date_x, y_mid, date_x, y1))
    # upper-row captions (top-left of each sub-cell), values left blank for entry.
    T(L_x + pad, y1 - cap_in, "Drawn", CAP, va="top")
    T(name_x + pad, y1 - cap_in, "Checked", CAP, va="top")
    T(date_x + pad, y1 - cap_in, "Date", CAP, va="top")
    # lower row: Title caption + the full identifier (centred in the row body)
    T(L_x + pad, y_mid - cap_in, "Title", CAP, va="top")
    if title:
        _fit_title(T, str(title), (L_x + xm) / 2.0, y0 + 0.22 * H,
                   cell_w=desc_w - 2 * pad, max_size=V + 1.0, min_size=3.2)

    # --- RIGHT (meta) zone --------------------------------------------------
    M_x0 = xm
    lines.append((M_x0, y_mid, x1, y_mid))
    # lower row split into 3 cells: Scale | Sheet | Drawing No.
    c1 = M_x0 + meta_w * 0.40
    c2 = M_x0 + meta_w * 0.68
    lines.append((c1, y0, c1, y_mid))
    lines.append((c2, y0, c2, y_mid))

    def lbl_val(xa, xb, label, value, vbold=False):
        T(xa + pad, y_mid - cap_in, label, CAP, va="top")
        if value is not None and value != "":
            cw = (xb - xa) - 2 * pad
            sz = V
            while sz > 2.8 and 0.52 * sz * len(str(value)) > cw:
                sz -= 0.3
            T(xa + pad, y0 + 0.22 * H, str(value), sz, bold=vbold)

    sc_txt = scale_label(_snap_std_scale(scale))
    if s_iso is not None:
        s_iso_disp = _snap_std_scale(s_iso)
        if abs(s_iso_disp - _snap_std_scale(scale)) > 1e-9:
            sc_txt += f" (ISO {scale_label(s_iso_disp)})"
    # Dwg No. left BLANK on purpose (user: do not dump the raw uuid/hash into the
    # title block). A real drawing number is assigned by the document system; the
    # generated dataset has none, so the cell stays empty for hand entry.
    dno = ""
    lbl_val(M_x0, c1, "Scale", sc_txt, vbold=True)
    lbl_val(c1, c2, "Sheet", paper)
    lbl_val(c2, x1, "Dwg No.", dno)

    # upper meta row: projection-method symbol + "ISO 5456-2 / 1st angle", the WHOLE
    # group CENTRED (horizontally + vertically) in the upper-right meta cell. The
    # _proj_symbol_lines glyph (trapezoid + concentric circles) spans ~6.2*r wide,
    # centred on its cx -- so the group width = that glyph width + gap + caption
    # width, and we centre the whole group (glyph then caption) in the cell.
    cell_cx = (M_x0 + x1) / 2.0
    cell_cy = y_mid + 0.5 * (y1 - y_mid)
    psr = min(2.6, (y1 - y_mid) * 0.26, meta_w * 0.085)  # symbol radius
    sym_w = 6.2 * psr                                     # full glyph width (~6.2r)
    cap_txt_w = 0.52 * CAP * len("ISO 5456-2")           # widest caption line
    gap = max(1.5, meta_w * 0.05)
    group_w = sym_w + gap + cap_txt_w
    g_left = cell_cx - group_w / 2.0
    sym_cx = g_left + sym_w / 2.0                         # glyph centred on its mid
    sym_cy = cell_cy
    txt_x = g_left + sym_w + gap                          # caption block left edge
    T(txt_x, cell_cy + CAP * 0.62, "ISO 5456-2", CAP, va="center")
    T(txt_x, cell_cy - CAP * 0.62, "1st angle", CAP, va="center")
    psym_at = (sym_cx, sym_cy, psr)

    return lines, texts, psym_at


def _proj_symbol_lines(cx, cy, r=4.0, first_angle=True):
    """ISO 5456-2 投影法识别符号: 一个截头圆锥(frustum)的两个正投影视图 ——
    侧视图(梯形/锥台轮廓) + 端视图(同心圆: 大端外圆 + 小端内圆 + 十字中心线)。
    第一角(标准): 梯形在左, 其 **大端(高边)朝向圆(朝右/朝内)**, 小端(矮边)朝外;
                  同心圆在右。梯形也带一条水平中心点画线(回转体轴线)。
    第三角(镜像): 同心圆在左, 梯形在右, 大端仍朝向圆(朝左)。
    返回 (thick_segs, thin_segs): 轮廓粗实线 thick + 中心线 thin(渲染为点画线)。"""
    import math
    thick, thin = [], []
    R = r            # 大端半径(端视图外圆)
    rr = r * 0.55    # 小端半径(端视图内圆)
    half_w = r * 1.25  # 梯形/端视图各自半宽
    gap = r * 0.55   # 梯形与同心圆之间的间隙

    def circles(ox, oy):
        for rad in (R, rr):
            pts = [(ox+rad*math.cos(2*math.pi*i/40), oy+rad*math.sin(2*math.pi*i/40))
                   for i in range(41)]
            for i in range(len(pts)-1):
                thick.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))
        # 圆心十字中心线(略超出外圆, 点画线) -> ⊕
        cl = R + r * 0.35
        thin.append((ox - cl, oy, ox + cl, oy))
        thin.append((ox, oy - cl, ox, oy + cl))

    def trapezoid(ox, big_on_left):
        # 梯形: 一端高 2R(大端), 一端高 2rr(小端); 上下两条斜边 + 两条竖边。
        xl, xr = ox - half_w, ox + half_w
        if big_on_left:
            hl, hr = R, rr           # 大端在左
        else:
            hl, hr = rr, R           # 大端在右
        thick.extend([
            (xl, oy_+hl, xr, oy_+hr),   # 上斜边
            (xl, oy_-hl, xr, oy_-hr),   # 下斜边
            (xl, oy_-hl, xl, oy_+hl),   # 左竖边
            (xr, oy_-hr, xr, oy_+hr),   # 右竖边
        ])
        # 梯形水平中心轴线(点画线, 略伸出两端) -> 表明这是回转体侧视图
        ext = r * 0.35
        thin.append((xl - ext, oy_, xr + ext, oy_))

    oy_ = cy
    if first_angle:
        # 梯形在左(大端朝右/朝向圆, 小端朝外/朝左), 同心圆在右
        tx = cx - (half_w + gap)
        ccx = cx + (half_w + gap)
        trapezoid(tx, big_on_left=False)
        circles(ccx, cy)
    else:
        # 第三角: 同心圆在左, 梯形在右(大端朝左/朝向圆, 小端朝外/朝右)
        ccx = cx - (half_w + gap)
        tx = cx + (half_w + gap)
        circles(ccx, cy)
        trapezoid(tx, big_on_left=True)
    return thick, thin


def _render_mpl(segs, uuid, paper, scale, proj, pw, ph, out_prefix, fmts, results, labels, s_iso=None, dims=None, centerlines=None, marks=None, balloon_art=None, bom_art=None, bearing_art=None, thread_art=None, mass=None, title=None, table=None):
    fig = plt.figure(figsize=(pw/25.4, ph/25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, pw); ax.set_ylim(0, ph); ax.set_aspect("equal"); ax.axis("off")

    for name, kind, x0, y0, x1, y1 in segs:
        if kind == "visible":
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.5, solid_capstyle="round")
        else:
            ax.plot([x0, x1], [y0, y1], color="0.55", lw=0.35, ls=(0, (3, 2)))

    frame, tb = _frame_lines(pw, ph, table)
    for (x0, y0, x1, y1) in frame:
        ax.plot([x0, x1], [y0, y1], color="black", lw=1.0)

    tbx, tby0, tbx1, tby1 = tb
    # ISO 7200 title-block: ruled table + standard fields (empty cells stay blank).
    # Title = full identifier (uuid / part name), Mass in kg (None -> blank cell).
    tb_lines, tb_texts, (psx, psy, psr) = _titleblock(
        pw, ph, uuid, paper, scale, s_iso,
        title=(title or uuid or None), mass=mass, table=table)
    for (x0, y0, x1, y1) in tb_lines:
        ax.plot([x0, x1], [y0, y1], color="black", lw=0.5)
    for (x, y, t, size, ha, va, bold) in tb_texts:
        ax.text(x, y, t, fontsize=size, ha=ha, va=va,
                fontweight="bold" if bold else "normal")
    # projection-method symbol inside its title-block cell: outline thick solid,
    # centre lines (circle cross + trapezoid axis) as dash-dot (ISO centreline).
    psym_thick, psym_thin = _proj_symbol_lines(psx, psy, r=psr, first_angle=True)
    for (x0, y0, x1, y1) in psym_thin:
        ax.plot([x0, x1], [y0, y1], color="black", lw=0.35,
                ls=(0, (6, 1.5, 1, 1.5)))
    for (x0, y0, x1, y1) in psym_thick:
        ax.plot([x0, x1], [y0, y1], color="black", lw=0.8)

    # view labels under each ortho/iso view
    names = {"front": "FRONT", "top": "TOP", "left": "LEFT", "iso": "ISO"}
    if marks:
        names[marks["label_view"]] = "A-A"        # sectioned view retitled
    for name, lab in names.items():
        bx = labels.get(name)
        if bx:
            ax.text(bx[0], bx[1], lab, fontsize=5.5, ha="center", va="top", color="black")

    # SECTION artwork: hatch (thin solid), cutting-line end strokes (thick),
    # sight arrows (filled), 'A' letters -- ISO 128-44/50.
    if marks:
        for (x0, y0, x1, y1) in marks["hatch"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.3)
        for (x0, y0, x1, y1) in marks["strokes"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=1.2)
        for (x, y, dx, dy) in marks["arrows"]:
            L, W = 4.0, 1.4
            tip = (x + dx * L, y + dy * L)
            bl = (x - dy * W / 2, y + dx * W / 2)
            br = (x + dy * W / 2, y - dx * W / 2)
            ax.fill([bl[0], br[0], tip[0]], [bl[1], br[1], tip[1]], color="black")
        for (x, y, t) in marks["texts"]:
            ax.text(x, y, t, fontsize=6.5, ha="center", va="center",
                    color="black", fontweight="bold")

    # Swept-path CENTRELINE (ISO 128 dash-dot, black). Drawn ON TOP (high zorder)
    # so the spine still reads where it runs along the solid's own outline.
    for (_v, poly) in (centerlines or []):
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        ax.plot(xs, ys, color="black", lw=0.6, ls=(0, (8, 2, 1, 2)),
                zorder=5)

    # ISO 8826 bearing symbols (thick outline / thin centre & element symbol)
    if bearing_art:
        for (x0, y0, x1, y1) in bearing_art["thick"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.5,
                    solid_capstyle="round", zorder=4)
        for (x0, y0, x1, y1) in bearing_art["thin"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.25, zorder=4)
    # ISO 6410 conventional thread lines (always fine/thin)
    if thread_art:
        for (x0, y0, x1, y1) in thread_art["thin"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.25, zorder=4)

    # ISO 129-1 dimensions
    for dm in (dims or []):
        for (x0, y0, x1, y1) in dm["thin"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.25)
        for (x0, y0, x1, y1) in dm["arrow"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.6)
        tx, ty, txt, rot, va, ha = dm["text"]
        # ISO 3098: dimension text ~3.5 mm tall. The figure is sized in inches
        # (= mm/25.4) so 1 pt = 0.353 mm -> ~10 pt gives a readable 3.5 mm.
        ax.text(tx, ty, txt, fontsize=10, rotation=rot, va=va, ha=ha)

    # ASSEMBLY: item balloons (ISO 6433)
    if balloon_art:
        import matplotlib.patches as mpatches
        for (x, y, r) in balloon_art["dots"]:
            ax.add_patch(mpatches.Circle((x, y), r, color="black", zorder=6))
        for (x0, y0, x1, y1) in balloon_art["leaders"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.35, zorder=6)
        for (cx, cy, r) in balloon_art["circles"]:
            ax.add_patch(mpatches.Circle((cx, cy), r, fill=True, facecolor="white",
                                         edgecolor="black", lw=0.6, zorder=7))
        for (cx, cy, t) in balloon_art["texts"]:
            ax.text(cx, cy, t, fontsize=9, ha="center", va="center",
                    zorder=8, fontweight="bold")
    # ASSEMBLY: parts list / BOM (ISO 7573)
    if bom_art:
        for (x0, y0, x1, y1) in bom_art["lines"]:
            ax.plot([x0, x1], [y0, y1], color="black", lw=0.35)
        for (x, y, t, hdr, ha, size) in bom_art["texts"]:
            ax.text(x, y, t, fontsize=size, ha=ha, va="center",
                    fontweight="bold" if hdr else "normal")

    if "png" in fmts:
        p = out_prefix + ".png"
        fig.savefig(p, dpi=200)
        results["png"] = p
    if "svg" in fmts:
        p = out_prefix + ".svg"
        fig.savefig(p)
        results["svg"] = p
    plt.close(fig)


def _render_dxf(segs, uuid, paper, scale, proj, pw, ph, out_prefix, results, labels, s_iso=None, dims=None, centerlines=None, marks=None, bearing_art=None, thread_art=None, mass=None, title=None, table=None):
    doc = ezdxf.new("R2010")
    doc.layers.add("VISIBLE", color=7)
    doc.layers.add("HIDDEN", color=8, linetype="DASHED")
    doc.layers.add("FRAME", color=5)
    doc.layers.add("TEXT", color=3)
    doc.layers.add("DIM", color=1)
    doc.layers.add("CENTER", color=4, linetype="CENTER")
    doc.layers.add("HATCH", color=7)
    msp = doc.modelspace()
    for name, kind, x0, y0, x1, y1 in segs:
        layer = "VISIBLE" if kind == "visible" else "HIDDEN"
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": layer})
    # SECTION artwork: hatch lines, cutting-line strokes, sight arrows, letters
    if marks:
        for (x0, y0, x1, y1) in marks["hatch"]:
            msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "HATCH"})
        for (x0, y0, x1, y1) in marks["strokes"]:
            msp.add_line((x0, y0), (x1, y1),
                         dxfattribs={"layer": "VISIBLE", "lineweight": 70})
        for (x, y, dx, dy) in marks["arrows"]:
            L = 4.0
            msp.add_line((x, y), (x + dx * L, y + dy * L),
                         dxfattribs={"layer": "VISIBLE"})
        for (x, y, t) in marks["texts"]:
            msp.add_text(t, dxfattribs={"layer": "TEXT", "height": 3.5}
                         ).set_placement((x, y))
    # swept-path centreline polylines
    for (_v, poly) in (centerlines or []):
        if len(poly) >= 2:
            msp.add_lwpolyline(poly, dxfattribs={"layer": "CENTER"})
    # ISO 8826 bearing symbols + ISO 6410 thread lines
    if bearing_art:
        for (x0, y0, x1, y1) in bearing_art["thick"]:
            msp.add_line((x0, y0), (x1, y1),
                         dxfattribs={"layer": "VISIBLE", "lineweight": 50})
        for (x0, y0, x1, y1) in bearing_art["thin"]:
            msp.add_line((x0, y0), (x1, y1),
                         dxfattribs={"layer": "VISIBLE", "lineweight": 18})
    if thread_art:
        for (x0, y0, x1, y1) in thread_art["thin"]:
            msp.add_line((x0, y0), (x1, y1),
                         dxfattribs={"layer": "VISIBLE", "lineweight": 18})
    frame, tb = _frame_lines(pw, ph, table)
    for (x0, y0, x1, y1) in frame:
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "FRAME"})
    tbx, tby0, tbx1, tby1 = tb
    # ISO 7200 title-block grid + fields
    tb_lines, tb_texts, (psx, psy, psr) = _titleblock(
        pw, ph, uuid, paper, scale, s_iso,
        title=(title or uuid or None), mass=mass, table=table)
    for (x0, y0, x1, y1) in tb_lines:
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "FRAME"})
    for (x, y, t, size, ha, va, bold) in tb_texts:
        if not t:
            continue
        h = max(1.8, size * 0.55)          # mpl pt -> ~mm text height
        align = (ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER if ha == "center"
                 else ezdxf.enums.TextEntityAlignment.MIDDLE_LEFT)
        msp.add_text(t, dxfattribs={"layer": "TEXT", "height": h}
                     ).set_placement((x, y), align=align)
    psym_thick, psym_thin = _proj_symbol_lines(psx, psy, r=psr, first_angle=True)
    for (x0, y0, x1, y1) in psym_thick:
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "FRAME"})
    for (x0, y0, x1, y1) in psym_thin:
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "CENTER"})
    names = {"front": "FRONT", "top": "TOP", "left": "LEFT", "iso": "ISO"}
    if marks:
        names[marks["label_view"]] = "A-A"
    for name, lab in names.items():
        bx = labels.get(name)
        if bx:
            msp.add_text(lab, dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((bx[0], bx[1]), align=ezdxf.enums.TextEntityAlignment.TOP_CENTER)
    # ISO 129-1 dimensions on their own layer
    for dm in (dims or []):
        for (x0, y0, x1, y1) in dm["thin"] + dm["arrow"]:
            msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "DIM"})
        tx, ty, txt, rot, va, ha = dm["text"]
        te = msp.add_text(txt, dxfattribs={"layer": "DIM", "height": 2.5, "rotation": rot})
        te.set_placement((tx, ty))
    p = out_prefix + ".dxf"
    doc.saveas(p)
    results["dxf"] = p


def scale_label(scale):
    """ISO 5455 scale designation. scale = paper_mm / model_mm.
    >1 magnification -> 'N:1' ; <1 reduction -> '1:N' ; ==1 -> '1:1'."""
    if abs(scale - 1.0) < 1e-6:
        return "1:1"
    if scale > 1.0:
        n = scale
        return f"{_num(n)}:1"
    else:
        n = 1.0 / scale
        return f"1:{_num(n)}"


def _snap_std_scale(scale):
    """Snap a continuous scale factor (paper_mm/model_mm) to the nearest standard
    ISO 5455 ratio so the title block never displays an illegal value like
    '1.01:1'. Snapping is done in log space (ratios are multiplicative), choosing
    the closest preferred ratio. The drawing itself may still use the continuous
    factor; only the DISPLAYED designation is snapped."""
    if scale <= 0:
        return 1.0
    import math
    best = min(STD_SCALES, key=lambda s: abs(math.log(scale) - math.log(s)))
    return float(best)


def _num(v):
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.3g}"


# backward-compat alias used by callers expecting "1:X" suffix form
def _scale_str(scale):
    return scale_label(scale).split(":", 1)[-1] if scale <= 1 else scale_label(scale)
