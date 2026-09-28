# -*- coding: utf-8 -*-
"""Post-pass for DXF sheets rendered BEFORE the writer fix of 2026-09-28: add the ISO 128-20
line-type definitions (DASHED, CENTER) to the LTYPE table, set the layer line weights and
switch line-weight display on -- exactly the definitions drawing._render_dxf now writes.
Geometry and entities are untouched. Used for the assembly sheets (1m_Convert/assemblies,
1m_Convert/two_part_assemblies), which are not re-laid-out; the part sheets are regenerated.
Usage (cadfit-env): python -X utf8 fix_dxf_tables.py <dir> [<dir> ...]
"""
import glob, os, sys, time
import ezdxf

LTYPES = {"DASHED": ([5.25, 4.2, -1.05], "ISO 128-20 dashed __ __ __ __ __ __"),
          "CENTER": ([7.75, 6.0, -0.75, 0.25, -0.75], "ISO 128-20 long-dashed dotted ____ . ____ . ____")}
WEIGHTS = {"VISIBLE": 50, "HIDDEN": 25, "FRAME": 50, "TEXT": 25, "DIM": 25, "CENTER": 25, "HATCH": 25}


def fix(path):
    doc = ezdxf.readfile(path)
    changed = False
    for name, (pat, desc) in LTYPES.items():
        if name not in doc.linetypes:
            doc.linetypes.add(name, pattern=pat, description=desc); changed = True
    for name, w in WEIGHTS.items():
        if name in doc.layers:
            lay = doc.layers.get(name)
            if lay.dxf.lineweight != w:
                lay.dxf.lineweight = w; changed = True
    if doc.header.get("$LWDISPLAY", 0) != 1:
        doc.header["$LWDISPLAY"] = 1; changed = True
    if changed:
        doc.saveas(path)
    return changed


def main():
    t0 = time.time(); n = c = f = 0
    for d in sys.argv[1:]:
        for p in sorted(glob.glob(os.path.join(d, "*", "drawing.dxf"))):
            n += 1
            try:
                c += fix(p)
            except Exception as e:
                f += 1; print("FAIL", p, repr(e)[:100], flush=True)
            if n % 200 == 0:
                print("%d files, %d changed, %d failed, %.0fs" % (n, c, f, time.time() - t0), flush=True)
    print("DONE files=%d changed=%d failed=%d %.0fs" % (n, c, f, time.time() - t0))


if __name__ == "__main__":
    main()
