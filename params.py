"""
Extract named build parameters (name -> numeric value) from a part's py script
and metadata.json. Three source formats seen in this dataset:
  1) Measures(...) keywords in cadquery_ops_json  (e.g. block_width=80.0)
  2) top-level named assignments in the py  (e.g. handle_length = 100.0)
  3) bare literals in calls (e.g. box(10,10,1)) -> no names, skipped here
Returns a dict {name: float}. Names feed iso_knowledge.classify_param.
"""
import json
import os
import re


def from_metadata(folder):
    p = os.path.join(folder, "metadata.json")
    out = {}
    if not os.path.isfile(p):
        return out
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return out
    for op in d.get("cadquery_ops_json") or []:
        if not isinstance(op, dict):
            continue
        if op.get("op_name") == "Measures":
            for kw in op.get("keywords", []):
                name = kw.get("arg")
                val = kw.get("value")
                try:
                    out[name] = float(val)
                except (TypeError, ValueError):
                    pass
    return out


_ASSIGN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([-+]?\d+\.?\d*)\s*(?:#.*)?$",
                     re.M)

# Class-attribute params, e.g. a Measures/Params class whose __init__ sets
#   self.width = 50.0
#   self.bore_diameter = 8.0
# The leading `self.` and indentation make _ASSIGN (anchored at column 0) miss
# them, so a whole class-based build script comes back with zero parameters.
# Capture the attribute NAME (after self.) and its numeric literal.
_SELF_ASSIGN = re.compile(
    r"^\s+self\.([a-zA-Z_]\w*)\s*=\s*([-+]?\d+\.?\d*)\s*(?:#.*)?$", re.M)

# Keyword-style `name=value` parameters, e.g. a params bag built with
# SimpleNamespace/dict:  p = NS(linear_width=50.0, block_depth=15.0, ...).
# These are NOT top-level assignments (they are indented kwargs ending in , or ))
# so _ASSIGN misses them and the whole part comes back with zero parameters.
_KWARG = re.compile(r"\b([a-zA-Z_]\w*)\s*=\s*([-+]?\d+\.?\d*)\s*[,)]")

# cadquery API keyword arguments that are CONSTRUCTION controls, not part
# dimensions. _KWARG would otherwise capture e.g. polarArray(startAngle=0,
# angle=360, count=4) and try to dimension a bogus 0-deg / 360-deg angle. Exact
# lowercase name match only, so a real design param like `groove_angle` is kept.
_KWARG_SKIP = {
    "startangle", "angle", "count", "n", "num", "segments", "rotate",
    "centeroption", "clean", "combine", "forconstruction", "makesolid",
    "isfrenet", "transition", "both", "offset", "tol", "tolerance",
    "anglesstep", "angularstep",
}

# A .chamfer(...) / .bevel(...) call whose FIRST argument is a bare numeric
# literal (e.g. `.chamfer(0.5)` or `.chamfer(0.5, 0.2887)`) carries no named
# parameter, so the normal assignment scan misses it and the chamfer never gets
# a C<size> callout. Capture that first literal as a synthetic chamfer size.
# (When the first arg is a variable name like `.chamfer(chamfer_size)`, the
# assignment scan already picks up the value, so this only fires on literals.)
_CHAMFER_LIT = re.compile(r"\.(?:chamfer|bevel)\s*\(\s*([-+]?\d+\.?\d*)\b")


def from_script(folder):
    p = os.path.join(folder, "cadquery.py")
    out = {}
    if not os.path.isfile(p):
        return out
    src = open(p, encoding="utf-8").read()
    for m in _ASSIGN.finditer(src):
        name, val = m.group(1), m.group(2)
        try:
            out[name] = float(val)
        except ValueError:
            pass
    # Class-attribute params (self.<name> = <num> inside a Measures/Params class).
    for m in _SELF_ASSIGN.finditer(src):
        name, val = m.group(1), m.group(2)
        if name in out:
            continue
        try:
            out[name] = float(val)
        except ValueError:
            pass
    # Fallback: keyword-style params (NS/dict bag). Only fill names not already
    # found as top-level assignments, so an explicit assignment always wins, and
    # drop cadquery construction kwargs that are not part dimensions.
    for m in _KWARG.finditer(src):
        name, val = m.group(1), m.group(2)
        if name in out or name.lower() in _KWARG_SKIP:
            continue
        try:
            out[name] = float(val)
        except ValueError:
            pass
    # Synthesize chamfer sizes from bare-literal .chamfer()/.bevel() calls. Use
    # the FIRST arg (the primary chamfer leg). Number multiple distinct calls so
    # several literal chamfers each get their own param name.
    seen = []
    for m in _CHAMFER_LIT.finditer(src):
        try:
            v = float(m.group(1))
        except ValueError:
            continue
        if v <= 0:
            continue
        # de-dup identical sizes (same chamfer applied via .edges().chamfer(c))
        if any(abs(v - s) < 1e-6 for s in seen):
            continue
        seen.append(v)
        key = "chamfer_size" if len(seen) == 1 else f"chamfer_size_{len(seen)}"
        out.setdefault(key, v)
    return out


def extract(folder):
    """Merge both sources (script names take priority if duplicated)."""
    params = {}
    params.update(from_metadata(folder))
    params.update(from_script(folder))
    return params
