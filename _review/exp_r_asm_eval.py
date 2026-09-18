# -*- coding: utf-8 -*-
"""实验R (装配闭环) 评测: 预测的放置块 vs 真值放置块, 103 件测试装配体.
指标:
  * exec: 放置块 + 固定前言 (原脚本的 import/_load_part/base/result) 能执行并得到 >=1 个实体;
  * n_bodies: 结果复合体的实体数 (真值 = 1 + 3 x 紧固件数, 两件装配 +1);
  * fastener count exact; 紧固件 (kind, size) 多重集 P/R/F1; 同类紧固件位置误差 (贪心最近匹配, mm) 中位数 / <=1 mm 命中率;
  * 轴向正确率; 两件装配 partB 平移误差 (mm).
基线 (released cadrille): 输出为单实体零件程序, 不含 fastener()/place() -> 全部为 0, 仍按同一解析器评.
用法: conda run -n cadquery python exp_r_asm_eval.py <pred_dir_name> [...]   (predictions/<name>/<asm_name>.py)
"""
import os, sys, ast, json, re
import numpy as np
ROOT = r'E:/3005/data'
sys.path.insert(0, os.path.join(ROOT, '_review'))
from guarded_exec import run_guarded_batch
ASM = os.path.join(ROOT, '_review', 'cc_asm')
SRC = {'single': os.path.join(ROOT, '1m_Convert', 'assemblies_slim'), 'two': os.path.join(ROOT, '1m_Convert', 'two_part_assemblies_slim')}
names = [l.strip() for l in open(os.path.join(ASM, 'test_names.txt')) if l.strip()]


def asm_dir(name):
    return os.path.join(SRC['two' if name.endswith('__two') else 'single'], name)


def preamble(name):
    src = open(os.path.join(asm_dir(name), 'assembly_cadquery.py'), encoding='utf-8').read().split('\n')
    end = max(i for i, l in enumerate(src) if re.match(r"^base\w* = _load_part\(", l)) + 1
    head = '\n'.join(src[:end]).replace("_HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()",
                                        "_HERE = r'%s'" % asm_dir(name).replace('/', os.sep))
    return head + '\n'


RESULT_LINE = "result = cq.Compound.makeCompound([p.val() if hasattr(p, 'val') else p for p in parts])\n"


def parse_block(code):
    """返回 (fasteners=[(kind,size,axis,point)], partB_translation or None, parse_ok)."""
    try:
        t = ast.parse(code)
    except Exception:
        return [], None, False
    fs, trans = [], None
    for n in ast.walk(t):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'place':
            try:
                fc = n.args[0]
                assert isinstance(fc, ast.Call) and fc.func.id == 'fastener'
                kind = ast.literal_eval(fc.args[0]); size = ast.literal_eval(fc.args[1])
                kw = {k.arg: ast.literal_eval(k.value) for k in n.keywords if k.arg in ('axis', 'point')}
                fs.append((kind, str(size), tuple(float(x) for x in kw['axis']), tuple(float(x) for x in kw['point'])))
            except Exception:
                continue
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'SetValues' and len(n.args) == 12:
            try:
                v = [ast.literal_eval(a) if not isinstance(a, ast.UnaryOp) else -ast.literal_eval(a.operand) for a in n.args]
                trans = (float(v[3]), float(v[7]), float(v[11]))
            except Exception:
                pass
    return fs, trans, True


def probe(shape):
    try:
        import cadquery as cq
        s = shape
        n = len(cq.Shape(s).Solids()) if not isinstance(s, cq.Shape) else len(s.Solids())
    except Exception:
        n = -1
    return dict(n_solids=n)


def match_positions(gt, pr):
    """同 kind 的贪心最近匹配; 返回位置误差列表 (mm) 和轴向一致数."""
    errs, axis_ok = [], 0
    used = set()
    for g in gt:
        best, bi = None, None
        for i, p in enumerate(pr):
            if i in used or p[0] != g[0]:
                continue
            d = float(np.linalg.norm(np.array(p[3]) - np.array(g[3])))
            if best is None or d < best:
                best, bi = d, i
        if bi is not None:
            used.add(bi); errs.append(best)
            if abs(abs(float(np.dot(pr[bi][2], g[2]))) - 1) < 1e-3:
                axis_ok += 1
    return errs, axis_ok


def evaluate(pred_name):
    pdir = os.path.join(ROOT, 'predictions', pred_name)
    recs, exec_items = [], []
    for nm in names:
        pf = os.path.join(pdir, nm + '.py')
        if not os.path.isfile(pf):
            continue
        code = open(pf, encoding='utf-8', errors='replace').read()
        exec_items.append((nm, preamble(nm) + code + '\n' + RESULT_LINE))
    ex = run_guarded_batch(exec_items, 'exp_r_asm_eval', 'probe', mem_gb=3.0, per_item_timeout=120, batch_size=5)
    tp = fp = fn = 0; cnt_exact = 0; errs_all = []; axis_ok = axis_n = 0; trans_errs = []; n_exec = 0; body_exact = 0
    for nm, _ in exec_items:
        code = open(os.path.join(pdir, nm + '.py'), encoding='utf-8', errors='replace').read()
        gt = open(os.path.join(ASM, 'code', nm + '.py'), encoding='utf-8').read()
        gfs, gtr, _ = parse_block(gt); pfs, ptr, ok_parse = parse_block(code)
        ok, payload = ex.get(nm, (False, 'no result'))
        n_solids = payload['n_solids'] if ok and isinstance(payload, dict) else 0
        if ok and n_solids >= 1:
            n_exec += 1
        gt_bodies = (2 if nm.endswith('__two') else 1) + len(gfs)
        if ok and n_solids == gt_bodies:
            body_exact += 1
        from collections import Counter
        cg, cp = Counter((k, s) for k, s, _, _ in gfs), Counter((k, s) for k, s, _, _ in pfs)
        inter = sum((cg & cp).values()); tp += inter; fp += sum(cp.values()) - inter; fn += sum(cg.values()) - inter
        if len(gfs) == len(pfs):
            cnt_exact += 1
        e, a = match_positions(gfs, pfs); errs_all += e; axis_ok += a; axis_n += len(e)
        if gtr is not None and ptr is not None:
            trans_errs.append(float(np.linalg.norm(np.array(ptr) - np.array(gtr))))
        recs.append(dict(name=nm, exec=bool(ok and n_solids >= 1), n_solids=n_solids, gt_bodies=gt_bodies, n_gt=len(gfs), n_pred=len(pfs),
                         pos_err=e, err=None if ok else str(payload)[:80]))
    n = len(exec_items)
    P = tp / max(1, tp + fp); R = tp / max(1, tp + fn)
    e = np.array(errs_all) if errs_all else np.array([np.nan])
    out = dict(method=pred_name, n=n, exec_rate=round(n_exec / max(1, n), 4), body_count_exact=round(body_exact / max(1, n), 4),
               fastener_count_exact=round(cnt_exact / max(1, n), 4), fastener_type_P=round(P, 4), fastener_type_R=round(R, 4),
               fastener_type_F1=round(2 * P * R / max(1e-9, P + R), 4), n_matched=len(errs_all),
               pos_err_median_mm=round(float(np.nanmedian(e)), 3), pos_within_1mm=round(float(np.mean(e <= 1.0)), 4) if errs_all else None,
               axis_correct=round(axis_ok / max(1, axis_n), 4), partB_trans_err_median_mm=round(float(np.median(trans_errs)), 3) if trans_errs else None,
               n_two_with_transform=len(trans_errs),
               gt_fasteners_total=tp + fn, pred_fasteners_total=tp + fp)
    return out, recs


if __name__ == '__main__':
    pj = os.path.join(ROOT, '_review', 'exp_r_asm.json')
    prev = json.load(open(pj)) if os.path.exists(pj) else {}
    for name in sys.argv[1:]:
        o, r = evaluate(name); prev[name] = o
        print(json.dumps(o, indent=1), flush=True)
        json.dump(r, open(os.path.join(ROOT, '_review', 'exp_r_records_%s.json' % name), 'w'), indent=1)
    json.dump(prev, open(pj, 'w'), indent=1)
