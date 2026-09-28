"""Regenerate drawing.{png,svg,dxf} for EVERY part under output/ that has a
model.step. Applies the dimension-dedup / concentric-radius / anti-overlap fixes
in drawing.py. Resilient: per-part errors are logged and skipped. Progress is
printed every PROGRESS_EVERY parts so a tail/Monitor can follow it.
"""
import os
import sys
import time
import traceback

import make_drawings

OUT = "output"
PROGRESS_EVERY = 50


SKIP_FILE = "output_missing_drawings.txt"   # parts whose hidden-line removal exceeded 30 min


def uuids():
    skip = set()
    if os.path.isfile(SKIP_FILE):
        skip = {l.strip() for l in open(SKIP_FILE) if l.strip()}
    us = []
    for d in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, d)
        if d in skip:
            continue
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "model.step")):
            us.append(d)
    return us


def main():
    us = uuids()
    start = 0
    if len(sys.argv) > 1 and sys.argv[1].endswith(".txt"):   # explicit uuid list
        us = [l.strip() for l in open(sys.argv[1]) if l.strip()]
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    if len(sys.argv) > 1:            # optional resume offset
        start = int(sys.argv[1])
    us = us[start:]
    if len(sys.argv) > 2:            # optional count limit
        us = us[:int(sys.argv[2])]
    total = len(us)
    print(f"REGEN START total={total} (offset={start})", flush=True)
    ok = fail = 0
    t0 = time.time()
    for i, u in enumerate(us):
        try:
            make_drawings.process(u)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {u}: {e}", flush=True)
            traceback.print_exc()
        if (i + 1) % PROGRESS_EVERY == 0 or (i + 1) == total:
            dt = time.time() - t0
            rate = (i + 1) / dt if dt else 0
            eta = (total - (i + 1)) / rate if rate else 0
            print(f"PROGRESS {i+1}/{total} ok={ok} fail={fail} "
                  f"{rate:.2f}/s ETA={eta/60:.1f}min", flush=True)
    dt = time.time() - t0
    print(f"REGEN DONE ok={ok} fail={fail} elapsed={dt/60:.1f}min", flush=True)


if __name__ == "__main__":
    main()
