# -*- coding: utf-8 -*-
"""Parameter extraction and classification of the TEXT modality, frozen at the version that
produced the released descriptions (2026-06-07) and passed the human review of 200 descriptions
(every quoted value correct and correctly classed, radius vs diameter, angle vs distance).

The drawing generator later extended iso_knowledge.classify_param (a *_radius -> diameter
qualifier and sweep|sector|arc_ angle keywords) and params.from_script (a self.<name> = <num>
scan). Those changes serve the drawings; for the text they would re-class radii as diameters.
augment_data.build_description therefore uses extract() and classify_param() from this module.
Reconstruction validated byte for byte against every released description
(_review/_restore20/validate_desc_0607.py)."""
import os, re
import params as P
import iso_knowledge as K

_RULES_0607 = [(r"(angle|_deg|degree|taper)" if kind == K.KIND_ANGLE else pat, kind, sym)
               for pat, kind, sym in K._RULES]


def classify_param(name):
    n = name.lower(); last = n.rsplit("_", 1)[-1]
    if last in ("x", "y", "z") and "_" in n[:-2]:
        last = n[:-2].rstrip("_").rsplit("_", 1)[-1]
    if ("chamfer" in n or "bevel" in n) and last not in ("angle", "deg", "degree"):
        return K.KIND_CHAMFER, K._SYM[K.KIND_CHAMFER], K.PREFER_VIEWS[K.KIND_CHAMFER]
    if last in K._SUFFIX:
        kind = K._SUFFIX[last]
        return kind, K._SYM[kind], K.PREFER_VIEWS[kind]
    for pat, kind, sym in _RULES_0607:
        if re.search(pat, n):
            return kind, sym, K.PREFER_VIEWS[kind]
    return None


def from_script(folder):
    p = os.path.join(folder, "cadquery.py"); out = {}
    if not os.path.isfile(p):
        return out
    src = open(p, encoding="utf-8").read()
    for m in P._ASSIGN.finditer(src):
        try: out[m.group(1)] = float(m.group(2))
        except ValueError: pass
    for m in P._KWARG.finditer(src):
        name = m.group(1)
        if name in out or name.lower() in P._KWARG_SKIP:
            continue
        try: out[name] = float(m.group(2))
        except ValueError: pass
    seen = []
    for m in P._CHAMFER_LIT.finditer(src):
        try: v = float(m.group(1))
        except ValueError: continue
        if v <= 0 or any(abs(v - s) < 1e-6 for s in seen):
            continue
        seen.append(v)
        out.setdefault("chamfer_size" if len(seen) == 1 else f"chamfer_size_{len(seen)}", v)
    return out


def extract(folder):
    """params.extract with the June script scanner: metadata first, script names win."""
    out = {}
    out.update(P.from_metadata(folder))
    out.update(from_script(folder))
    return out


def install():
    """Patch params / iso_knowledge in place (used by the 2026-09 validation scripts)."""
    K.classify_param = classify_param
    P.from_script = from_script
