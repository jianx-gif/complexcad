"""批量预处理 stl_data 中尚未处理的真实件 -> grabcad_in/(逐件子进程+600s超时)。
已处理过的 10 个源文件(旧命名规则)直接跳过。"""
import os, re, subprocess, sys

SRC = "E:/3005/data/stl_data"
DST = "E:/3005/data/cadfit_repro/grabcad_in"
PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {
    "Assem Connecting Rod - 7.16-14-1.STL",
    "Assem Connecting Rod - 7.16-14-2.STL",
    "Assem Connecting Rod - Connecting Crank Bearing 1-1.STL",
    "Assem Connecting Rod - Connecting Crank Bearing 2-1.STL",
    "Assem Connecting Rod - Connecting Rod Design Down-1.STL",
    "Assem Connecting Rod - Connecting Rod Design Up-1.STL",
    "Assem Connecting Rod - Rod Bearing-1.STL",
    "Ball Stud throttle.STL",
    "C5 Knuckle Mesh Decimated.stl",
    "CONNECTING ROD ASSEMBLY.stl",
}

os.makedirs(DST, exist_ok=True)
seen = set()
for f in sorted(os.listdir(SRC)):
    if not f.lower().endswith(".stl") or f in SKIP:
        continue
    stem = os.path.splitext(f)[0]
    name = re.sub(r"[^A-Za-z0-9_-]", "_", stem)
    name = re.sub(r"_+", "_", name).strip("_")
    if name.lower() in seen:
        continue
    seen.add(name.lower())
    out = os.path.join(DST, name + ".stl")
    if os.path.isfile(out):
        print("SKIP-EXIST", name)
        continue
    try:
        r = subprocess.run([PY, "-X", "utf8", os.path.join(HERE, "prep_one.py"),
                            os.path.join(SRC, f), out],
                           capture_output=True, text=True, timeout=600)
        tail = (r.stdout or "").strip().splitlines()
        print(name, "|", tail[-1] if tail else ("rc=%d %s" % (r.returncode, (r.stderr or "")[-80:])))
    except subprocess.TimeoutExpired:
        print(name, "| PREP-TIMEOUT-600s")
        if os.path.isfile(out):
            os.remove(out)
print("prep_batch done")
