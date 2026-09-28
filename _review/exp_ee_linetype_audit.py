# -*- coding: utf-8 -*-
"""实验EE: ISO 128 线型审计 (批注 p40 #99: 规则表缺线型与剖面线). 并行版, 每张图只遍历一次实体.
对全部释出 drawing.dxf:
  * 图层线型名是否符合 ISO 128 用法: VISIBLE=连续, HIDDEN=虚线, CENTER=点划线
  * 这些线型在 DXF 线型表里是否有定义 (没有定义则 CAD 软件按连续线画)
  * 线宽: 图层线宽是否设置 (-1/-2/-3 = 未设置); 可见轮廓线实体是否带线宽
  * 有隐藏线、剖面线的图纸数
  * 中心线分开统计: 扫掠路径中心线 (CENTER 层 LWPOLYLINE) 与装配轴线 / 投影符号 (CENTER 层 LINE).
    单件图的投影符号固定画在标题栏, 所以 CENTER 层 LINE 不能当作"零件有中心线".
    另统计: 图上是否存在整圆轮廓 (VISIBLE 层闭合折线段近似的圆无法直接识别, 故用 metadata 的孔数代替, 见 has_hole)
另外把 drawing.py 里 PNG/SVG 渲染线宽写进结果 (matplotlib 线宽单位是 pt, 1 pt = 0.3528 mm).
用法 (cadfit-env): python exp_ee_linetype_audit.py
"""
import os, json, collections
from multiprocessing import Pool

R = r'E:/3005/data'
OUT = os.path.join(R, 'output')
PT = 25.4 / 72


def one(u):
    import ezdxf
    p = os.path.join(OUT, u, 'drawing.dxf')
    try:
        d = ezdxf.readfile(p)
    except Exception:
        return {'unreadable': 1}
    c = collections.Counter()
    lay = {l.dxf.name: l for l in d.layers}
    defined = {lt.dxf.name.upper() for lt in d.linetypes}
    vis = lay['VISIBLE'].dxf.linetype.upper() if 'VISIBLE' in lay else ''
    hid = lay['HIDDEN'].dxf.linetype.upper() if 'HIDDEN' in lay else ''
    cen = lay['CENTER'].dxf.linetype.upper() if 'CENTER' in lay else ''
    c['sheets'] = 1
    c['layer_linetype_names_iso'] = int(vis == 'CONTINUOUS' and 'DASH' in hid and 'CENTER' in cen)
    c['hidden_linetype_defined'] = int(hid in defined)
    c['center_linetype_defined'] = int(cen in defined)
    c['linetype_table_only_default'] = int(defined <= {'CONTINUOUS', 'BYLAYER', 'BYBLOCK'})
    wts = {l.dxf.lineweight for l in d.layers if l.dxf.name in ('VISIBLE', 'HIDDEN', 'CENTER', 'DIM', 'HATCH')}
    c['layer_lineweights_set'] = int(any(w not in (-1, -2, -3) for w in wts))
    seen = collections.Counter()
    vis_w = collections.Counter()
    for e in d.modelspace():
        t = e.dxftype()
        ly = e.dxf.layer
        seen[(t, ly)] += 1
        if t == 'LINE' and ly == 'VISIBLE':
            vis_w[e.dxf.get('lineweight', -1)] += 1
    n_vis = sum(vis_w.values())
    c['visible_lines'] = n_vis
    c['visible_lines_with_weight'] = sum(v for k, v in vis_w.items() if k not in (-1, -2, -3))
    c['sheets_with_hidden_lines'] = int(seen[('LINE', 'HIDDEN')] > 0)
    c['sheets_with_hatch'] = int(seen[('LINE', 'HATCH')] > 0 or any(k[0] == 'HATCH' for k in seen))
    c['sheets_with_sweep_centreline'] = int(seen[('LWPOLYLINE', 'CENTER')] > 0)
    c['center_layer_line_entities'] = seen[('LINE', 'CENTER')]
    c['sheets_center_lines_gt_symbol'] = 0  # filled below once the symbol count is known
    c['_cl_%d' % seen[('LINE', 'CENTER')]] = 1
    # holes / cylinders from the metadata (does the part have a feature that would carry a centre line?)
    try:
        m = json.load(open(os.path.join(OUT, u, 'metadata.json'), encoding='utf-8'))
        ops = [o.get('op_name', '') for o in (m.get('cadquery_ops_json') or []) if isinstance(o, dict)]
        c['parts_with_hole_op'] = int(any(o in ('hole', 'cboreHole', 'cskHole') for o in ops))
        c['parts_with_revolve_or_cylinder'] = int(any(o in ('revolve', 'cylinder', 'circle') for o in ops))
    except Exception:
        c['metadata_unreadable'] = 1
    return dict(c)


if __name__ == '__main__':
    uu = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'drawing.dxf')))
    tot = collections.Counter()
    with Pool(8) as pool:
        for r in pool.imap_unordered(one, uu, chunksize=50):
            tot.update(r)
    hist = {k[4:]: v for k, v in tot.items() if k.startswith('_cl_')}
    res = {'n_sheets': tot['sheets']}
    res.update({k: v for k, v in tot.items() if k != 'sheets' and not k.startswith('_cl_')})
    res['center_layer_line_count_histogram'] = dict(sorted(hist.items(), key=lambda kv: int(kv[0])))
    res['sheets_center_lines_gt_symbol'] = sum(v for k, v in hist.items() if int(k) > min(int(x) for x in hist))
    res['visible_lines_with_weight_share'] = round(tot['visible_lines_with_weight'] / max(1, tot['visible_lines']), 6)
    # PNG/SVG line widths as coded in drawing.py::_render_mpl (pt -> mm)
    res['raster_line_widths_mm'] = {
        'visible_outline': round(0.71 * PT, 3), 'hidden_dashed': round(0.37 * PT, 3),
        'dimension': round(0.37 * PT, 3), 'hatch': round(0.37 * PT, 3),
        'sweep_centreline_dashdot': round(0.37 * PT, 3), 'symbol_centreline_dashdot': round(0.37 * PT, 3),
        'hole_centreline_dashdot': round(0.37 * PT, 3),
        'frame': round(1.0 * PT, 3), 'section_cutting_stroke': round(1.2 * PT, 3)}
    json.dump(res, open(os.path.join(R, '_review', 'exp_ee_linetype_audit.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))
