# -*- coding: utf-8 -*-
"""实验DD: 策展时排除的 20 个上游程序, 现在逐个执行并检查论文所述的结构条件
(单一连通实体、正体积、至少 7 个面), 记录实际失败在哪一步 (批注 #73 要求按原因计数).
两步:  (1) t2cq 环境 (有 pyarrow):  python exp_dd_excluded20.py extract
       (2) cadfit-env (有 psutil):   python exp_dd_excluded20.py run
"""
import os, sys, json, collections
R = r'E:/3005/data'
CODES = os.path.join(R, '_review', 'excluded20_codes.json')


def probe(shape):
    from OCP.TopExp import TopExp
    from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID, TopAbs_SHELL
    from OCP.TopTools import TopTools_IndexedMapOfShape
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.BRepCheck import BRepCheck_Analyzer
    out = {}
    for t, k in ((TopAbs_FACE, 'faces'), (TopAbs_SOLID, 'solids'), (TopAbs_SHELL, 'shells')):
        m = TopTools_IndexedMapOfShape(); TopExp.MapShapes_s(shape, t, m); out[k] = m.Extent()
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, g); out['volume'] = round(g.Mass(), 3)
    out['brepcheck'] = bool(BRepCheck_Analyzer(shape, True).IsValid())
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'extract':
        sys.path.insert(0, os.path.join(R, '1m_Convert'))
        import dataset_source
        import pyarrow.parquet as pq
        rel = {json.loads(l)['uuid'] for l in open(os.path.join(R, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')}
        codes = {}
        for f in dataset_source.parquet_files():
            pf = pq.ParquetFile(f)
            for rg in range(pf.num_row_groups):
                for r in pf.read_row_group(rg, columns=['uuid', 'cadquery_file', 'num_faces']).to_pylist():
                    if r['uuid'] not in rel:
                        c = r['cadquery_file']
                        if isinstance(c, (bytes, bytearray)):
                            c = bytes(c).decode('utf-8', 'replace')
                        codes[r['uuid']] = dict(code=c, upstream_faces=r['num_faces'])
        json.dump(codes, open(CODES, 'w', encoding='utf-8'))
        print('extracted', len(codes))
    else:
        sys.path.insert(0, os.path.join(R, '_review'))
        from guarded_exec import run_guarded_batch
        codes = json.load(open(CODES, encoding='utf-8'))
        res = run_guarded_batch([(u, d['code']) for u, d in codes.items()], 'exp_dd_excluded20', 'probe',
                                mem_gb=3.0, per_item_timeout=120)
        why = collections.Counter(); recs = {}
        for u, (ok, p) in res.items():
            if not ok:
                reason = 'execution error: ' + str(p).split(':')[0]
            elif p['solids'] != 1:
                reason = 'not a single solid (%d solids)' % p['solids']
            elif p['volume'] <= 0:
                reason = 'non-positive volume'
            elif p['faces'] < 7:
                reason = 'fewer than 7 faces'
            else:
                reason = 'passes all three now'
            why[reason] += 1
            recs[u] = dict(ok=ok, probe=p, reason=reason, upstream_faces=codes[u]['upstream_faces'])
        json.dump(dict(reasons=dict(why), records=recs), open(os.path.join(R, '_review', 'exp_dd_excluded20.json'), 'w'), indent=1)
        print(dict(why))
        for u, r in recs.items():
            print(u[:8], r['reason'], r['probe'] if r['ok'] else '')
