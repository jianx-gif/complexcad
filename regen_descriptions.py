"""Rebuild description.json / description.txt (the TEXT modality) for every part
under output/<uuid>/ WITHOUT touching the other modalities.

Reads metadata.json (cadquery_ops_json, geometry_stats) and the build script and
re-runs augment_data.build_description, so the fix of the step list (construction
order, no 2D sketch primitives; see augment_data._real_ops) reaches every part.
Usage:  python -X utf8 regen_descriptions.py [output_dir]
"""
import json
import os
import sys
import time

import augment_data as ad

OUT = sys.argv[1] if len(sys.argv) > 1 else "output"


def main():
    ad.OUT = OUT
    us = sorted(d for d in os.listdir(OUT)
                if os.path.isfile(os.path.join(OUT, d, "metadata.json")))
    t0 = time.time()
    ok = fail = 0
    for i, u in enumerate(us):
        folder = os.path.join(OUT, u)
        try:
            meta = json.load(open(os.path.join(folder, "metadata.json"), encoding="utf-8"))
            stats = meta.get("geometry_stats")
            if not stats:
                raise RuntimeError("no geometry_stats in metadata.json")
            structured, free_text = ad.build_description(
                folder, meta.get("cadquery_ops_json"), stats)
            json.dump(structured, open(os.path.join(folder, "description.json"), "w",
                                       encoding="utf-8"), indent=2, ensure_ascii=False)
            open(os.path.join(folder, "description.txt"), "w",
                 encoding="utf-8").write(free_text + "\n")
            ok += 1
        except Exception as e:
            fail += 1
            print("FAIL %s: %s" % (u, e), flush=True)
        if (i + 1) % 1000 == 0 or (i + 1) == len(us):
            print("%d/%d ok=%d fail=%d %.0fs" % (i + 1, len(us), ok, fail, time.time() - t0),
                  flush=True)


if __name__ == "__main__":
    main()
