"""防崩评分驱动: 每个预测放**独立子进程 + 硬超时**跑 score_one.py, 低并发(2)。
畸形几何/死循环/爆内存最多影响到点被杀的那个子进程, 绝不拖垮系统。纯 CPU, 不碰 GPU。
用法: python score_safe.py <method> <names_file> [--jobs 2] [--timeout 4]
输出: precision_report/pred_metrics_<method>.jsonl + 打印分层汇总。
"""
import sys, os, json, time, subprocess, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ROOT = os.path.dirname(PARENT)
REPORT = os.path.join(PARENT, "precision_report")
SCORE_ONE = os.path.join(HERE, "score_one.py")
PY = sys.executable


def score_one(args):
    uuid, pred_path, timeout = args
    try:
        cp = subprocess.run([PY, "-X", "utf8", SCORE_ONE, uuid, pred_path],
                            timeout=timeout, capture_output=True, text=True)
        for line in reversed(cp.stdout.splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    return json.loads(line)
                except Exception:
                    pass
        return {"uuid": uuid, "valid": False, "status": "no_output"}
    except subprocess.TimeoutExpired:
        return {"uuid": uuid, "valid": False, "status": "timeout"}
    except Exception as e:
        return {"uuid": uuid, "valid": False, "status": "drv_err:" + str(e)[:40]}


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else float("nan")


def summarize(recs, method):
    def bucket(rs, label):
        ok = [r for r in rs if r.get("status") == "ok"]
        print("  %-9s N=%-4d valid=%.1f%%  CD=%.4f  F=%.3f  opType=%.2f opCount=%.2f exact=%.1f%%"
              % (label, len(rs), 100 * _mean([r.get("valid", False) for r in rs]),
                 _mean([r.get("chamfer") for r in ok]), _mean([r.get("fscore") for r in ok]),
                 _mean([r.get("op_type_recall") for r in rs]),
                 _mean([r.get("op_count_recall") for r in rs]),
                 100 * _mean([r.get("op_exact") for r in rs])), flush=True)
    print("\n===== 方法 [%s] 汇总 (n=%d) =====" % (method, len(recs)), flush=True)
    bucket(recs, "ALL")
    bucket([r for r in recs if not r.get("complex")], "simple")
    bucket([r for r in recs if r.get("complex")], "complex")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("names_file")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=4)
    args = ap.parse_args()
    os.makedirs(REPORT, exist_ok=True)

    pred_dir = os.path.join(ROOT, "predictions", args.method)
    uuids = [l.strip() for l in open(args.names_file, encoding="utf-8") if l.strip()]
    tasks = [(u, os.path.join(pred_dir, u + ".py"), args.timeout)
             for u in uuids if os.path.isfile(os.path.join(pred_dir, u + ".py"))]
    print("防崩评分 %d 件 (jobs=%d, 每件独立子进程超时 %ds, 纯CPU)"
          % (len(tasks), args.jobs, args.timeout), flush=True)

    recs = []; t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(score_one, t) for t in tasks]
        for i, f in enumerate(as_completed(futs), 1):
            recs.append(f.result())
            if i % 40 == 0:
                print("  %d/%d  %.2fs/件  ETA %.1fmin"
                      % (i, len(tasks), (time.time() - t0) / i,
                         (len(tasks) - i) * (time.time() - t0) / i / 60), flush=True)
    out = os.path.join(REPORT, "pred_metrics_%s.jsonl" % args.method)
    open(out, "w", encoding="utf-8").write(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in recs))
    st = {}
    for r in recs:
        st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
    print("状态分布: %s" % st, flush=True)
    summarize(recs, args.method)
    print("\n-> %s  用时 %.1fmin" % (out, (time.time() - t0) / 60), flush=True)


if __name__ == "__main__":
    main()
