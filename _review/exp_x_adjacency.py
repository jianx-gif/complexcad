# -*- coding: utf-8 -*-
"""实验X: 拓扑「邻接」一致性, 而不只是实体计数一致 (批注 p44 #122/#128).

导师指出: F/E/V 计数相等并不能证明拓扑相同. 本实验对同一模型的两个实体
    A = 已释出的 model.brep (由上游 STEP 转换, 即上游环境的执行结果)
    B = 在本环境里重新执行 cadquery.py 得到的实体
比较两级签名:
  1. 计数签名      (F, E, V)
  2. 带标签邻接签名  —— 面邻接图的一阶 Weisfeiler-Lehman 标签多重集:
        每个面 -> (曲面类型, 该面的边数, 邻接面数, 邻接面曲面类型的有序多重集)
     再加边签名: 每条非退化边 -> (曲线类型, 相邻面数)
     两个多重集都相等才算邻接一致.
  邻接签名相等是同构的必要条件 (不是充分条件); 一旦不等, 就证明拓扑不同.
  关键数字: 计数相等的模型里, 有多少邻接签名也相等 —— 即"计数相等但拓扑不同"的比例.
用法 (cadquery 环境): python exp_x_adjacency.py [n]   默认 600, seed 42, 仅取可执行模型
输出: _review/exp_x_adjacency.json + _records.jsonl
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, json, random, hashlib

ROOT = _ROOT
OUT = os.path.join(ROOT, 'output')

from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopTools import TopTools_IndexedMapOfShape, TopTools_IndexedDataMapOfShapeListOfShape
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve


def _h(obj):
    return hashlib.sha1(repr(obj).encode()).hexdigest()[:16]


def signature(shape):
    """JSON-serialisable topology signature of a TopoDS_Shape (called inside the guarded worker too)."""
    fmap = TopTools_IndexedMapOfShape(); TopExp.MapShapes_s(shape, TopAbs_FACE, fmap)
    emap = TopTools_IndexedMapOfShape(); TopExp.MapShapes_s(shape, TopAbs_EDGE, emap)
    vmap = TopTools_IndexedMapOfShape(); TopExp.MapShapes_s(shape, TopAbs_VERTEX, vmap)
    nf = fmap.Extent()
    ftype = []
    for i in range(1, nf + 1):
        try:
            ftype.append(str(BRepAdaptor_Surface(TopoDS.Face_s(fmap.FindKey(i))).GetType()).split('.')[-1])
        except Exception:
            ftype.append('?')
    ef = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(shape, TopAbs_EDGE, TopAbs_FACE, ef)
    nbrs = [set() for _ in range(nf)]
    fedges = [0] * nf
    esig = []
    for i in range(1, ef.Extent() + 1):
        e = TopoDS.Edge_s(ef.FindKey(i))
        idx = set()
        for f in ef.FindFromIndex(i):
            k = fmap.FindIndex(f)
            if k > 0:
                idx.add(k - 1)
        for a in idx:
            fedges[a] += 1
            nbrs[a].update(b for b in idx if b != a)
        if BRep_Tool.Degenerated_s(e):
            continue
        try:
            ct = str(BRepAdaptor_Curve(e).GetType()).split('.')[-1]
        except Exception:
            ct = '?'
        esig.append((ct, len(idx)))
    fsig = sorted((ftype[i], fedges[i], len(nbrs[i]), tuple(sorted(ftype[j] for j in nbrs[i])))
                  for i in range(nf))
    deg = [len(nbrs[i]) for i in range(nf)]
    usig = sorted((fedges[i], deg[i], tuple(sorted(deg[j] for j in nbrs[i]))) for i in range(nf))
    uesig = sorted(k for _, k in esig)
    return dict(F=nf, E=emap.Extent(), V=vmap.Extent(), face=_h(fsig), edge=_h(sorted(esig)),
                topo=_h((usig, uesig)))


def brep_signature(uuid):
    from OCP.BRep import BRep_Builder
    from OCP.BRepTools import BRepTools
    from OCP.TopoDS import TopoDS_Shape
    s = TopoDS_Shape()
    if not BRepTools.Read_s(s, os.path.join(OUT, uuid, 'model.brep'), BRep_Builder()):
        return None
    return signature(s)


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(ROOT, '_review'))
    from guarded_exec import run_guarded_batch
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rows = [json.loads(l) for l in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'),
                                        encoding='utf-8')]
    pool = sorted(r['uuid'] for r in rows if r.get('valid')
                  and os.path.isfile(os.path.join(OUT, r['uuid'], 'model.brep')))
    random.seed(42)
    sample = random.sample(pool, min(n, len(pool)))
    meta = {r['uuid']: r for r in rows}

    items = [(u, open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read())
             for u in sample]
    print('re-executing', len(items), 'programs (guarded)...', flush=True)
    rex = run_guarded_batch(items, 'exp_x_adjacency', 'signature', mem_gb=3.0, per_item_timeout=90)

    recs = []
    for i, u in enumerate(sample, 1):
        ok, a = rex.get(u, (False, 'missing'))
        b = brep_signature(u)
        rec = dict(uuid=u, reexec_ok=bool(ok), brep_ok=b is not None)
        if ok and b is not None:
            ce = (a['F'], a['E'], a['V']) == (b['F'], b['E'], b['V'])
            fe = a['face'] == b['face']
            ee = a['edge'] == b['edge']
            te = a['topo'] == b['topo']
            rec.update(count_equal=ce, topo_equal=te, face_sig_equal=fe, edge_sig_equal=ee,
                       adjacency_equal=fe and ee,
                       reexec=[a['F'], a['E'], a['V']], brep=[b['F'], b['E'], b['V']])
        else:
            rec.update(err=str(a)[:80] if not ok else 'brep-read')
        recs.append(rec)
        if i % 100 == 0:
            print(i, '/', len(sample), flush=True)
    with open(os.path.join(ROOT, '_review', 'exp_x_adjacency_records.jsonl'), 'w', encoding='utf-8') as fo:
        for r in recs:
            fo.write(json.dumps(r) + '\n')

    pairs = [r for r in recs if 'count_equal' in r]
    ce = [r for r in pairs if r['count_equal']]
    ae = [r for r in pairs if r['adjacency_equal']]
    ce_not_ae = [r for r in ce if not r['adjacency_equal']]
    ae_not_ce = [r for r in ae if not r['count_equal']]
    te = [r for r in pairs if r['topo_equal']]
    ce_not_te = [r for r in ce if not r['topo_equal']]
    te_not_ae = [r for r in te if not r['adjacency_equal']]
    summary = dict(
        n_sampled=len(sample), n_pairs=len(pairs),
        reexec_failed=sum(1 for r in recs if not r['reexec_ok']),
        count_equal=len(ce), count_equal_rate=round(len(ce) / max(1, len(pairs)), 4),
        adjacency_equal=len(ae), adjacency_equal_rate=round(len(ae) / max(1, len(pairs)), 4),
        face_sig_equal=sum(1 for r in pairs if r['face_sig_equal']),
        edge_sig_equal=sum(1 for r in pairs if r['edge_sig_equal']),
        count_equal_but_adjacency_differs=len(ce_not_ae),
        share_of_count_equal_with_same_adjacency=round((len(ce) - len(ce_not_ae)) / max(1, len(ce)), 4),
        adjacency_equal_but_counts_differ=len(ae_not_ce),
        unlabelled_topology_equal=len(te), unlabelled_topology_equal_rate=round(len(te) / max(1, len(pairs)), 4),
        count_equal_but_topology_differs=len(ce_not_te),
        share_of_count_equal_with_same_topology=round((len(ce) - len(ce_not_te)) / max(1, len(ce)), 4),
        same_topology_but_surface_types_differ=len(te_not_ae),
        sample=dict(seed=42, pool='executing models with a released model.brep', n=len(pool)))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_x_adjacency.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
