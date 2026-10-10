# -*- coding: utf-8 -*-
"""实验GG: HLR 投影把一条直边切成多少段 (批注 p35 #98: 定义并量化, 否则删除).
对 seed 42 抽的 200 张释出图纸, 把 VISIBLE 图层上的 LINE 按"共线且首尾相接(0.01 mm)"合并成链,
统计每条直边(链)由几段组成: 被切成 >=2 段的直边占比、每条直边段数的中位数/P95/最大值.
用法 (cadfit-env): python exp_gg_hlr_fragments.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json, random, math, collections
import ezdxf

R = _ROOT
OUT = os.path.join(R, 'output')
uu = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'drawing.dxf')))
random.seed(42)
sample = random.sample(uu, 200)
TOL = 0.01


def key(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        return None
    ux, uy = dx / L, dy / L
    if ux < -1e-9 or (abs(ux) < 1e-9 and uy < 0):
        ux, uy = -ux, -uy
    # line: direction + signed distance of the carrier line from origin
    c = round(-uy * p[0] + ux * p[1], 2)
    return (round(ux, 4), round(uy, 4), c)


chain_sizes = []
for u in sample:
    d = ezdxf.readfile(os.path.join(OUT, u, 'drawing.dxf'))
    groups = collections.defaultdict(list)
    for e in d.modelspace().query('LINE'):
        if e.dxf.layer != 'VISIBLE':
            continue
        p, q = (e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)
        k = key(p, q)
        if k is None:
            continue
        ux, uy, _ = k
        t0, t1 = sorted((p[0] * ux + p[1] * uy, q[0] * ux + q[1] * uy))
        groups[k].append((t0, t1))
    for segs in groups.values():
        segs.sort()
        cur_n, cur_end = 1, segs[0][1]
        for a, b in segs[1:]:
            if a <= cur_end + TOL:          # touches or overlaps: same straight edge
                cur_n += 1; cur_end = max(cur_end, b)
            else:
                chain_sizes.append(cur_n); cur_n, cur_end = 1, b
        chain_sizes.append(cur_n)
cs = sorted(chain_sizes)
res = dict(n_sheets=len(sample), straight_edges=len(cs), split_into_2_or_more=sum(1 for x in cs if x >= 2),
           share_split=round(sum(1 for x in cs if x >= 2) / len(cs), 4), median_segments=cs[len(cs) // 2],
           p95_segments=cs[int(.95 * len(cs))], max_segments=cs[-1], mean_segments=round(sum(cs) / len(cs), 2))
json.dump(res, open(os.path.join(R, '_review', 'exp_gg_hlr_fragments.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
