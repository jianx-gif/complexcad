# -*- coding: utf-8 -*-
"""实验T: 工程图自动规则审计 (ISO 129-1 / ISO 3098 / ISO 5455 / ISO 5456-2 可机检的部分), 跑满所有 output/<uuid>/drawing.dxf.
每张图:
  * 尺寸完整性: 程序里每个尺寸类具名参数 (直径/半径/倒角/线性/角度) 是否以相容类型出现在图上的尺寸文字里 (⌀v / Rv / Cv / v / v°; 半径参数也接受 ⌀2v);
  * 文字压线 (ISO 129-1: 尺寸文字不得被任何线穿过): DIM 文字包围盒 (内缩 0.3 mm) 与 VISIBLE/HIDDEN/CENTER 线、其它 DIM 线、其它 DIM 文字、标题栏是否相交;
  * 重复标注: 同 (类型, 值) 的尺寸文字在同一张图上出现 >1 次 (排除 "nx" 组合标注);
  * 文字高度是否属于 ISO 3098 系列 {1.8, 2.5, 3.5, 5, 7, 10};
  * 标题栏: Title/Scale/Sheet/Dwg No. 字段齐全, 比例字符串含 ISO 5455 系列值, 投影法标注 (ISO 5456-2, 1st angle), 视图标签 (FRONT/TOP/LEFT/ISO).
输出: _review/exp_t_drawing_audit.json (汇总) + exp_t_drawing_audit_records.jsonl (逐图).
用法: conda run -n cadfit-env python exp_t_drawing_audit.py [--limit N]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, re, json, math, glob, collections
import ezdxf
ROOT = _ROOT; OUT = os.path.join(ROOT, 'output')
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
ISO_H = (1.8, 2.5, 3.5, 5.0, 7.0, 10.0)
ISO_SCALES = {'1:1', '1:2', '1:5', '1:10', '1:20', '1:50', '1:100', '1:200', '1:500', '1:1000', '2:1', '5:1', '10:1', '20:1', '50:1'}
DIM_RE = re.compile(r"^(?:(\d+)x\s*)?([⌀ØRCM]?)\s*(-?\d+\.?\d*)\s*(°)?$")


def classify(name):
    low = name.lower()
    if any(k in low for k in ('count', 'num_', 'number', '_n_')) or low.startswith('n_'): return None
    if 'angle' in low: return 'angle'
    if 'chamfer' in low or 'bevel' in low: return 'chamfer'
    if 'dia' in low or 'bore' in low: return 'diameter'
    if 'radius' in low or 'fillet' in low or low.endswith('_r'): return 'radius'
    if any(k in low for k in ('depth', 'thick', 'width', 'length', 'height', 'spacing', 'offset', 'pitch', 'size', 'gap', 'span', 'dist')): return 'linear'
    return None


def parse_dim(text):
    t = text.strip().replace('Ø', '⌀')
    m = DIM_RE.match(t)
    if not m: return None
    mult, pre, val, deg = m.groups()
    v = float(val)
    kind = 'angle' if deg else {'⌀': 'diameter', 'R': 'radius', 'C': 'chamfer', 'M': 'thread'}.get(pre, 'linear')
    return kind, v, int(mult) if mult else 1


def text_bbox(e, margin=0.0):
    h = e.dxf.height; n = len(e.dxf.text); w = 0.72 * h * n
    x, y = e.dxf.insert.x, e.dxf.insert.y
    if abs((e.dxf.rotation or 0) - 90) < 1: box = (x - h, y, x, y + w)
    else: box = (x, y, x + w, y + h)
    return (box[0] + margin, box[1] + margin, box[2] - margin, box[3] - margin)


def seg_box_intersect(p, q, b):
    """线段 pq 与轴对齐盒 b 相交 (Liang-Barsky)."""
    x0, y0, x1, y1 = b
    if x1 <= x0 or y1 <= y0: return False
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pk) < 1e-12:
            if qk < 0: return False
        else:
            r = qk / pk
            if pk < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
            if t0 > t1: return False
    return True


def boxes_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def audit(uuid):
    dxf = os.path.join(OUT, uuid, 'drawing.dxf'); py = os.path.join(OUT, uuid, 'cadquery.py')
    if not (os.path.isfile(dxf) and os.path.isfile(py)): return None
    try:
        d = ezdxf.readfile(dxf)
    except Exception as e:
        return dict(uuid=uuid, error=str(e)[:80])
    msp = d.modelspace()
    lines = collections.defaultdict(list); texts = collections.defaultdict(list)
    for e in msp:
        if e.dxftype() == 'LINE': lines[e.dxf.layer].append(((e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)))
        elif e.dxftype() == 'TEXT': texts[e.dxf.layer].append(e)
    dims = [(t, parse_dim(t.dxf.text)) for t in texts['DIM']]
    parsed = [(t, p) for t, p in dims if p]
    # --- completeness
    params = [(n, float(v)) for n, v in PARAM_RE.findall(open(py, encoding='utf-8', errors='replace').read())]
    vals = collections.defaultdict(set)
    for _, (kind, v, mult) in parsed: vals[kind].add(round(v, 3))
    cov = collections.Counter(); tot = collections.Counter()
    for n, v in params:
        c = classify(n)
        if c is None or v <= 0: continue
        tot[c] += 1; v = round(v, 3)
        ok = (v in vals[c]) or (c == 'radius' and round(2 * v, 3) in vals['diameter']) or (c == 'linear' and (v in vals['diameter'] or v in vals['radius'])) \
             or (c == 'diameter' and round(v / 2, 3) in vals['radius'])
        if ok: cov[c] += 1
    # --- collisions
    view_lines = lines['VISIBLE'] + lines['HIDDEN'] + lines['CENTER']
    frame_box = None
    tb = [t for t in texts['TEXT'] if abs(t.dxf.height - 2.5) > 0.05]          # 标题栏字段 (视图标签高 2.5, 不算)
    if tb:
        xs = [t.dxf.insert.x for t in tb]; ys = [t.dxf.insert.y for t in tb]
        frame_box = (min(xs) - 2, min(ys) - 2, max(xs) + 30, max(ys) + 5)     # 标题栏区域近似
    col_view = col_dim = col_text = col_title = 0
    boxes = [text_bbox(t, 0.3) for t, _ in dims]
    for i, (t, _) in enumerate(dims):
        b = boxes[i]
        if any(seg_box_intersect(p, q, b) for p, q in view_lines): col_view += 1
        if any(seg_box_intersect(p, q, b) for p, q in lines['DIM']): col_dim += 1
        if any(boxes_overlap(b, boxes[j]) for j in range(len(dims)) if j != i): col_text += 1
        if frame_box and boxes_overlap(b, frame_box): col_title += 1
    # --- repeated dimensions
    cnt = collections.Counter((k, round(v, 3)) for _, (k, v, m) in parsed if m == 1)
    repeated = sum(1 for k, c in cnt.items() if c > 1)
    # --- text heights, title block, scale, projection, view labels
    heights = {round(t.dxf.height, 2) for lay in texts for t in texts[lay]}
    non_iso_h = sorted(h for h in heights if not any(abs(h - s) < 0.05 for s in ISO_H))
    tt = [t.dxf.text.strip() for t in texts['TEXT']]
    fields = {'Title': 'Title' in tt, 'Scale': 'Scale' in tt, 'Sheet': 'Sheet' in tt, 'DwgNo': any(x.startswith('Dwg') for x in tt)}
    scale_txt = next((x for x in tt if re.match(r'^\d+:\d+', x)), '')
    scale_iso = any(s in scale_txt for s in ISO_SCALES)
    projection = any('5456' in x for x in tt) and any('angle' in x for x in tt)
    labels = {x for x in tt if x in ('FRONT', 'TOP', 'LEFT', 'RIGHT', 'ISO', 'SECTION', 'A-A', 'B-B')}
    return dict(uuid=uuid, n_dims=len(dims), n_dims_parsed=len(parsed), n_params=sum(tot.values()), covered=sum(cov.values()),
                cov_by_class={c: [cov[c], tot[c]] for c in tot}, col_view=col_view, col_dim=col_dim, col_text=col_text, col_title=col_title,
                repeated=repeated, non_iso_heights=non_iso_h, fields_ok=all(fields.values()), scale=scale_txt, scale_iso=scale_iso,
                projection_note=projection, view_labels=sorted(labels))


if __name__ == '__main__':
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 0
    uuids = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'drawing.dxf')))
    if limit: uuids = uuids[:limit]
    recs = []; fo = open(os.path.join(ROOT, '_review', 'exp_t_drawing_audit_records.jsonl'), 'w', encoding='utf-8')
    for i, u in enumerate(uuids, 1):
        r = audit(u)
        if r: recs.append(r); fo.write(json.dumps(r, ensure_ascii=False) + '\n')
        if i % 500 == 0: print(i, '/', len(uuids), flush=True)
    fo.close()
    ok = [r for r in recs if 'error' not in r]
    n = len(ok)
    def rate(f): return round(sum(1 for r in ok if f(r)) / max(1, n), 4)
    cov_cls = collections.Counter(); tot_cls = collections.Counter()
    for r in ok:
        for c, (a, b) in r['cov_by_class'].items(): cov_cls[c] += a; tot_cls[c] += b
    summary = dict(n_drawings=n, n_errors=len(recs) - n,
                   dims_per_drawing_mean=round(sum(r['n_dims'] for r in ok) / max(1, n), 2),
                   dims_unparsed_share=round(sum(r['n_dims'] - r['n_dims_parsed'] for r in ok) / max(1, sum(r['n_dims'] for r in ok)), 4),
                   param_coverage=round(sum(r['covered'] for r in ok) / max(1, sum(r['n_params'] for r in ok)), 4),
                   param_coverage_by_class={c: dict(covered=cov_cls[c], total=tot_cls[c], rate=round(cov_cls[c] / max(1, tot_cls[c]), 4)) for c in tot_cls},
                   drawings_all_params_covered=rate(lambda r: r['covered'] == r['n_params']),
                   text_over_view_line=dict(drawings=rate(lambda r: r['col_view'] > 0), dims=round(sum(r['col_view'] for r in ok) / max(1, sum(r['n_dims'] for r in ok)), 4)),
                   text_crossed_by_dim_line=dict(drawings=rate(lambda r: r['col_dim'] > 0), dims=round(sum(r['col_dim'] for r in ok) / max(1, sum(r['n_dims'] for r in ok)), 4)),
                   text_text_overlap=dict(drawings=rate(lambda r: r['col_text'] > 0), dims=round(sum(r['col_text'] for r in ok) / max(1, sum(r['n_dims'] for r in ok)), 4)),
                   text_over_title_block=rate(lambda r: r['col_title'] > 0),
                   repeated_dimension=rate(lambda r: r['repeated'] > 0),
                   non_iso_text_height=rate(lambda r: len(r['non_iso_heights']) > 0),
                   non_iso_heights_seen=sorted({h for r in ok for h in r['non_iso_heights']}),
                   title_fields_complete=rate(lambda r: r['fields_ok']), scale_iso5455=rate(lambda r: r['scale_iso']),
                   projection_note=rate(lambda r: r['projection_note']),
                   three_views_labelled=rate(lambda r: {'FRONT', 'TOP', 'LEFT'} <= set(r['view_labels'])),
                   iso_view_present=rate(lambda r: 'ISO' in r['view_labels']))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_t_drawing_audit.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
