"""真实件 x 方法 几何指标+操作解析(cadfit-env: trimesh+scipy)。
对每个 <name>: 输入网格 = cadfit_repro/grabcad_run/<name>.stl
预测网格 = real_root/pred_stl/<method>/<name>.stl (exec_pred 产出)
CADFit 网格 = cadfit_repro/grabcad_run_runs/<name>/best_greedy_parallel_iterative.stl
独立归一化(与论文评分器一致) + CD/F(tau=0.02) + AST 解析操作。"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, ast, json
import numpy as np
import trimesh
from scipy.spatial import cKDTree

ROOT = _ROOT
REAL = f"{ROOT}/real_root"
GT = f"{ROOT}/cadfit_repro/grabcad_run"
TAU = 0.02
NAMES = [l.strip() for l in open(f"{REAL}/names.txt") if l.strip()]


def sample(path, n=8192):
    m = trimesh.load(path, force="mesh")
    pts, _ = trimesh.sample.sample_surface(m, n)
    return np.asarray(pts)


def norm(p):
    c = (p.min(0) + p.max(0)) / 2.0
    s = float((p.max(0) - p.min(0)).max()) + 1e-9
    return (p - c) / s


def cd_f(pred, gt):
    P, G = norm(pred), norm(gt)
    dPG, _ = cKDTree(G).query(P)
    dGP, _ = cKDTree(P).query(G)
    prec = float((dPG < TAU).mean()); rec = float((dGP < TAU).mean())
    return float(dPG.mean() + dGP.mean()), 2 * prec * rec / (prec + rec + 1e-9)


OPS = {"extrude", "revolve", "sweep", "loft", "fillet", "chamfer", "shell",
       "cut", "union", "add", "hole", "cskHole", "cboreHole"}


def parse_ops(pyfile):
    try:
        tree = ast.parse(open(pyfile, encoding="utf-8").read())
    except Exception:
        return "parse-err"
    cnt = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in OPS:
                cnt[node.func.attr] = cnt.get(node.func.attr, 0) + 1
    return " ".join(f"{k}x{v}" for k, v in sorted(cnt.items())) or "none"


rows = []
for n in NAMES:
    gt_pts = sample(f"{GT}/{n}.stl")
    for meth, stl, py in [
        ("cadrecode", f"{REAL}/pred_stl/cadrecode/{n}.stl", f"{REAL}/predictions/cadrecode/{n}.py"),
        ("cadrille",  f"{REAL}/pred_stl/cadrille/{n}.stl",  f"{REAL}/predictions/cadrille/{n}.py"),
        ("cadfit",    f"{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.stl",
                      f"{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.py"),
    ]:
        if not os.path.isfile(stl):
            rows.append((n, meth, None, None, "EXEC-FAIL"))
            continue
        try:
            cd, f = cd_f(sample(stl), gt_pts)
            rows.append((n, meth, cd, f, parse_ops(py)))
        except Exception as e:
            rows.append((n, meth, None, None, "ERR " + str(e)[:30]))

print("%-42s %-10s %7s %6s  %s" % ("part", "method", "CD", "F", "ops"))
for n, m, cd, f, ops in rows:
    print("%-42s %-10s %7s %6s  %s" % (n[:40], m,
          ("%.3f" % cd) if cd is not None else "--",
          ("%.2f" % f) if f is not None else "--", ops))
json.dump([{"part": n, "method": m, "cd": cd, "f": f, "ops": o}
           for n, m, cd, f, o in rows],
          open(f"{REAL}/real_metrics.json", "w"), indent=1)
print("saved real_metrics.json")
