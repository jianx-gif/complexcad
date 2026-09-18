"""全量重跑单件装配: 对每个已存在的 *__asm, 用最新代码(整圆孔+干涉检测+中心线
+ 工程图改进)重新产出, 覆盖。12 路子进程 + 单件超时。从件名解析 uuid 与 fastener。
"""
import os, sys, glob, subprocess, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ASM = os.path.join(HERE, "assemblies")
PY = sys.executable
TIMEOUT = 400
JOBS = 12


def parse(name):
    uuid = name.split("__")[0]
    fastener = "hex" if name[:-len("__asm")].endswith("_hex") else "socket"
    return uuid, fastener


def main():
    names = sorted(os.path.basename(d) for d in glob.glob(os.path.join(ASM, "*__asm"))
                   if os.path.isdir(d))
    print("全量重跑单件 %d (%d 路, 超时 %ds)" % (len(names), JOBS, TIMEOUT), flush=True)
    lock = threading.Lock()
    cnt = {"ok": 0, "fail": 0, "n": 0}

    def run(name):
        uuid, fastener = parse(name)
        out = ""
        try:
            cp = subprocess.run(
                [PY, "-X", "utf8", os.path.join(HERE, "produce_one.py"),
                 uuid, name, fastener],
                cwd=HERE, timeout=TIMEOUT, capture_output=True, text=True)
            ok = cp.returncode == 0 and "OK" in (cp.stdout or "")
            out = (cp.stdout or "")
        except subprocess.TimeoutExpired:
            ok = False
        # NORES = 新判据下该件装不了紧固件(干涉/整圆/无合适孔) -> 删除该件,
        # 不留旧装配图(它不该在装配数据集里)。
        nores = ("NORES" in out)
        with lock:
            cnt["n"] += 1
            if ok:
                cnt["ok"] += 1
            else:
                cnt["fail"] += 1
                if nores:
                    import shutil
                    shutil.rmtree(os.path.join(ASM, name), ignore_errors=True)
                    cnt["deleted"] = cnt.get("deleted", 0) + 1
            if cnt["n"] % 50 == 0:
                print("  %d/%d ok%d fail%d del%d" % (cnt["n"], len(names),
                      cnt["ok"], cnt["fail"], cnt.get("deleted", 0)), flush=True)

    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        futs = [ex.submit(run, n) for n in names]
        for _ in as_completed(futs):
            pass
    print("\n单件重跑完成: ok %d fail %d (其中NORES删除 %d) / %d"
          % (cnt["ok"], cnt["fail"], cnt.get("deleted", 0), len(names)), flush=True)


if __name__ == "__main__":
    main()
