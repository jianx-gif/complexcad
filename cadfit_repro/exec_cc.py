"""把 40 件 cc 子集的各方法预测代码执行成 STL -> cc_pred_stl/<method>/<uuid>.stl
(逐件子进程 + 90s 超时, 跳过已存在; 执行失败/超时留空 -> 渲染时标 invalid)。"""
import os, glob, subprocess, sys

ROOT = "E:/3005/data"
EXEC = f"{ROOT}/real_root/exec_pred.py"
DST = f"{ROOT}/cadfit_repro/cc_pred_stl"
METHODS = ["cadrecode", "cadrille", "zero2cad", "retrieval"]

uuids = [os.path.basename(d.rstrip("/\\"))
         for d in sorted(glob.glob(f"{ROOT}/cadfit_repro/cc_in_runs/*/"))]
print("uuids:", len(uuids))
for meth in METHODS:
    os.makedirs(f"{DST}/{meth}", exist_ok=True)
    ok = fail = skip = 0
    for u in uuids:
        src = f"{ROOT}/predictions/{meth}/{u}.py"
        out = f"{DST}/{meth}/{u}.stl"
        if os.path.isfile(out):
            skip += 1; continue
        if not os.path.isfile(src):
            fail += 1; continue
        try:
            r = subprocess.run(["python", "-X", "utf8", EXEC, src, out],
                               capture_output=True, timeout=90)
            if r.returncode == 0 and os.path.isfile(out):
                ok += 1
            else:
                fail += 1
        except subprocess.TimeoutExpired:
            fail += 1
            if os.path.isfile(out):
                os.remove(out)
    print(meth, "ok", ok, "fail", fail, "skip", skip, flush=True)
print("exec_cc done")
