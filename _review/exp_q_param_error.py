# -*- coding: utf-8 -*-
"""实验Q: 预测模型的建模精度 —— 参数误差 (尺寸/位置/角度层面的可测部分), 对闭环各方法统一测量.
对 400 件测试子集中每件:
  * 执行预测代码 -> B-rep; 记录可执行性;
  * 整体尺寸: 预测包围盒三边 (排序后) vs GT 包围盒三边: 绝对尺寸相对误差 (mm 尺度是否被恢复)
    与形状比例误差 (各边/最长边);
  * 特征参数: GT 程序中具名的 fillet / chamfer / diameter / depth 参数 (与实验G同分类),
    在预测几何(按 GT 最长边等比缩放后)上测同类特征 (圆柱半径/环面小半径/倒角带宽/圆柱轴向长度),
    误差 = 与最近候选之差; 报告 |err|<=0.1 mm / <=5% 命中率、中位误差、无候选特征(操作缺失)比例;
  * 可编辑性代理: 预测代码里的具名数值参数个数、以及是否含 5 种复杂操作调用.
用法 (任意带 psutil 的 python; 子进程用 cadquery env): python exp_q_param_error.py <pred_dir_name> [<pred_dir_name> ...]
"""
import os, sys, json, re, math, glob, ast, signal
import numpy as np
ROOT = r'E:/3005/data'
PRED = os.path.join(ROOT, 'predictions')
OUT = os.path.join(ROOT, 'output')
sys.path.insert(0, os.path.join(ROOT, '_review'))
from guarded_exec import run_guarded_batch
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Plane
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.gp import gp_Trsf, gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform

PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
OPS = {'loft', 'revolve', 'sweep', 'chamfer', 'fillet'}
test = [l.strip() for l in open(os.path.join(PRED, 'test_subset.txt'), encoding='utf-8') if l.strip()]
_GT_CACHE = {}


def classify(name):
    low = name.lower()
    if 'fillet' in low: return 'fillet'
    if 'chamfer' in low: return 'chamfer'
    if 'dia' in low or 'bore' in low: return 'diameter'
    if 'depth' in low: return 'depth'
    return None


def bbox(shape):
    b = Bnd_Box(); BRepBndLib.Add_s(shape, b, True)
    x0, y0, z0, x1, y1, z1 = b.Get()
    return [x1 - x0, y1 - y0, z1 - z0]


def features(shape):
    cyl_r, cyl_h, tor_r, plane_minext = [], [], [], []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current()); ad = BRepAdaptor_Surface(f); t = ad.GetType()
        u0, u1, v0, v1 = ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()
        if t == GeomAbs_Cylinder:
            cyl_r.append(ad.Cylinder().Radius())
            if all(map(math.isfinite, (v0, v1))): cyl_h.append(abs(v1 - v0))
        elif t == GeomAbs_Torus:
            tor_r.append(ad.Torus().MinorRadius())
        elif t == GeomAbs_Plane:
            if all(map(math.isfinite, (u0, u1, v0, v1))): plane_minext.append(min(abs(u1 - u0), abs(v1 - v0)))
        ex.Next()
    return cyl_r, cyl_h, tor_r, plane_minext


def probe(shape):
    """在受保护子进程里调用: 返回包围盒 + 特征列表 (可 JSON 化)."""
    return dict(bbox=bbox(shape), feats=features(shape))


def named_params(code):
    return [(nm, float(v)) for nm, v in PARAM_RE.findall(code)]


def ops_in(code):
    try:
        t = ast.parse(code)
    except Exception:
        return set()
    return {n.func.attr for n in ast.walk(t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in OPS}


def evaluate(pred_name):
    pdir = os.path.join(PRED, pred_name)
    recs = []
    cls_stats = {k: dict(attempted=0, hit_abs=0, hit_rel=0, no_candidate=0, errs=[]) for k in ('fillet', 'chamfer', 'diameter', 'depth')}
    dim_abs, dim_shape = [], []
    n_exec = n_named = n_total = 0
    n_fail_reason = {}
    # 批量受保护执行: 先 GT 程序 (缓存), 再预测程序
    global _GT_CACHE
    if not _GT_CACHE:
        gt_items = [(u, open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read()) for u in test]
        _GT_CACHE = run_guarded_batch(gt_items, 'exp_q_param_error', 'probe')
        print('  GT probed: ok %d / %d' % (sum(1 for v in _GT_CACHE.values() if v[0]), len(test)), flush=True)
    pred_items = []
    for u in test:
        pf = os.path.join(pdir, u + '.py')
        if os.path.isfile(pf):
            pred_items.append((u, open(pf, encoding='utf-8', errors='replace').read()))
    n_total = len(pred_items)
    pres = run_guarded_batch(pred_items, 'exp_q_param_error', 'probe')
    print('  predictions probed: ok %d / %d' % (sum(1 for v in pres.values() if v[0]), n_total), flush=True)
    for u, code in pred_items:
        gsrc = open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read()
        ok_g, rg = _GT_CACHE.get(u, (False, 'no gt'))
        ok_p, rp = pres.get(u, (False, 'no result'))
        if not (ok_g and ok_p):
            key = (rp if not ok_p else rg); key = key.split(':')[0][:40]
            n_fail_reason[key] = n_fail_reason.get(key, 0) + 1
            continue
        gb, pb = np.array(rg['bbox']), np.array(rp['bbox'])
        if pb.max() < 1e-6 or gb.max() < 1e-6:
            continue
        n_exec += 1
        if named_params(code): n_named += 1
        gs, pss = np.sort(gb)[::-1], np.sort(pb)[::-1]
        dim_abs.append(float(np.mean(np.abs(pss - gs) / np.maximum(gs, 1e-6))))
        dim_shape.append(float(np.mean(np.abs(pss / pss[0] - gs / gs[0]))))
        k = gs[0] / pss[0]
        cyl_r, cyl_h, tor_r, plane_minext = [[x * k for x in lst] for lst in rp['feats']]
        for nm, v in named_params(gsrc):
            c = classify(nm)
            if not c or v <= 0: continue
            st = cls_stats[c]; st['attempted'] += 1
            cand = {'diameter': [2 * r for r in cyl_r], 'fillet': cyl_r + tor_r, 'depth': cyl_h,
                    'chamfer': [w / math.sqrt(2) for w in plane_minext]}[c]
            if not cand:
                st['no_candidate'] += 1; continue
            err = min(abs(x - v) for x in cand); st['errs'].append(err)
            if err <= 0.1: st['hit_abs'] += 1
            if err <= 0.05 * v: st['hit_rel'] += 1
        recs.append(dict(uuid=u, ops_pred=sorted(ops_in(code)), ops_gt=sorted(ops_in(gsrc)), n_named=len(named_params(code))))
    out = dict(method=pred_name, n_predictions=n_total, n_executed=n_exec, failures=n_fail_reason,
               named_param_share=round(n_named / max(1, n_exec), 4),
               bbox_abs_rel_err_median=round(float(np.median(dim_abs)), 4) if dim_abs else None,
               bbox_shape_ratio_err_median=round(float(np.median(dim_shape)), 4) if dim_shape else None,
               bbox_abs_within_10pct=round(float(np.mean(np.array(dim_abs) <= 0.10)), 4) if dim_abs else None)
    for c, st in cls_stats.items():
        e = np.array(st['errs']) if st['errs'] else np.array([np.nan])
        out[c] = dict(attempted=st['attempted'], no_candidate=st['no_candidate'],
                      no_candidate_rate=round(st['no_candidate'] / max(1, st['attempted']), 4),
                      hit_0p1mm=round(st['hit_abs'] / max(1, st['attempted']), 4),
                      hit_5pct=round(st['hit_rel'] / max(1, st['attempted']), 4),
                      median_err_mm=round(float(np.nanmedian(e)), 4), p75_err_mm=round(float(np.nanquantile(e, 0.75)), 4))
    return out, recs


if __name__ == '__main__':
    res = {}
    for name in sys.argv[1:]:
        o, r = evaluate(name); res[name] = o
        print(json.dumps(o, indent=1), flush=True)
        json.dump(r, open(os.path.join(ROOT, '_review', 'exp_q_records_%s.json' % name), 'w'), indent=1)
    prev = {}
    pj = os.path.join(ROOT, '_review', 'exp_q_param_error.json')
    if os.path.exists(pj):
        prev = json.load(open(pj))
    prev.update(res)
    json.dump(prev, open(pj, 'w'), indent=1)
