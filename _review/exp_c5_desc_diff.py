# -*- coding: utf-8 -*-
"""实验C5: 新旧文本描述逐字段对照 (2026-09-28 修复只应改变步骤列表).

旧版 = 发布版 (2026-06-07 代码: text_params 的参数提取/分类 + 上游 ops 日志顺序、含草图基元的步骤表),
由 _review/_restore20/desc_0607.py 重建, 已对全部 9980 件逐字节验证. 新版 = 当前 output/<uuid>/description.*.
对每件比较:
  * parameters / parameter_groups / geometry / design_intent 字段是否完全相同
  * description.txt 去掉第一句 (步骤句) 后是否完全相同
  * 操作多重集: 旧版去掉草图基元后 与 新版 是否相同
用法 (cadfit-env): python -X utf8 exp_c5_desc_diff.py [output_dir]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import collections, json, os, sys

ROOT = _ROOT
sys.path.insert(0, ROOT); os.chdir(ROOT)
import augment_data as A

OUT = sys.argv[1] if len(sys.argv) > 1 else 'output'
SKETCH = {'circle', 'rect', 'polygon', 'polyline'}


def old_ops(ops_json):
    return [op.get('op_name') for op in ops_json or [] if op.get('op_name') in A._REAL_OPS]


def main():
    tot = collections.Counter(); ex = []
    for u in sorted(os.listdir(OUT)):
        folder = os.path.join(OUT, u)
        if not os.path.isfile(os.path.join(folder, 'description.json')):
            continue
        meta = json.load(open(os.path.join(folder, 'metadata.json'), encoding='utf-8'))
        new_st = json.load(open(os.path.join(folder, 'description.json'), encoding='utf-8'))
        new_tx = open(os.path.join(folder, 'description.txt'), encoding='utf-8').read().rstrip('\n')
        # old version: same function with the old step source
        saved = A.steps_from_source
        A.steps_from_source = lambda f, oj=None: old_ops(oj)
        try:
            old_st, old_tx = A.build_description(folder, meta.get('cadquery_ops_json'), meta['geometry_stats'])
        finally:
            A.steps_from_source = saved
        tot['n'] += 1
        same_fields = all(old_st[k] == new_st[k] for k in ('parameters', 'parameter_groups', 'geometry', 'design_intent'))
        tot['same_param_geom_intent'] += same_fields
        rest_old = old_tx.split('. ', 1)[1] if '. ' in old_tx else ''
        rest_new = new_tx.split('. ', 1)[1] if '. ' in new_tx else ''
        tot['same_text_after_step_sentence'] += (rest_old == rest_new)
        mo = collections.Counter(o for o in old_st['operation_sequence'] if o not in SKETCH)
        mn = collections.Counter(new_st['operation_sequence'])
        tot['same_3d_multiset'] += (mo == mn)
        tot['old_had_sketch_primitive'] += any(o in SKETCH for o in old_st['operation_sequence'])
        tot['order_changed_3d'] += ([o for o in old_st['operation_sequence'] if o not in SKETCH] != new_st['operation_sequence'])
        if not (same_fields and rest_old == rest_new and mo == mn) and len(ex) < 8:
            ex.append({'uuid': u[:8], 'fields': same_fields, 'text': rest_old == rest_new,
                       'old3d': dict(mo), 'new': dict(mn)})
    res = dict(tot); res['examples'] = ex
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(ROOT, '_review', 'exp_c5_desc_diff%s.json' % ('' if OUT == 'output' else '_' + os.path.basename(OUT))), 'w'), indent=1)


if __name__ == '__main__':
    main()
