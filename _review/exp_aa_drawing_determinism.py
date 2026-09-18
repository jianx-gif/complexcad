# -*- coding: utf-8 -*-
"""实验AA: 工程图可复现性实测 (附录声称 "重新生成的图纸与释出版本逐字节相同", 但从未实际重跑过).

取 seed 42 抽的 8 个模型, 把输入文件复制到临时目录, 让 make_drawings 在临时目录里重新出图,
再与释出的 drawing.dxf / drawing.svg 比较:
  * 字节是否完全相同 (sha256)
  * DXF: 去掉头部时间戳后, 实体 (类型, 图层, 坐标, 文字) 多重集是否相同
不会写 output/ 下的任何文件.
用法 (cadfit-env, 在项目根目录): python _review/exp_aa_drawing_determinism.py
"""
import os, sys, json, shutil, tempfile, hashlib, random
ROOT = r'E:/3005/data'
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import ezdxf
import make_drawings

rows = [json.loads(l) for l in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')]
pool = sorted(r['uuid'] for r in rows if r.get('valid') and os.path.isfile(os.path.join(ROOT, 'output', r['uuid'], 'drawing.dxf')))
random.seed(42)
sample = random.sample(pool, 8)
tmp = tempfile.mkdtemp(prefix='drw_')
make_drawings.OUT = tmp


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def dxf_entities(p):
    doc = ezdxf.readfile(p)
    out = []
    for e in doc.modelspace():
        t = e.dxftype(); lay = e.dxf.layer
        if t == 'LINE':
            v = tuple(round(x, 6) for x in (*e.dxf.start, *e.dxf.end))
        elif t in ('CIRCLE', 'ARC'):
            v = tuple(round(x, 6) for x in (*e.dxf.center, e.dxf.radius))
        elif t in ('TEXT', 'MTEXT'):
            v = (e.dxf.text if t == 'TEXT' else e.text, tuple(round(x, 6) for x in e.dxf.insert))
        else:
            v = ()
        out.append((t, lay, v))
    return sorted(out, key=repr)


res = []
for u in sample:
    src = os.path.join(ROOT, 'output', u)
    dst = os.path.join(tmp, u)
    os.makedirs(dst)
    for f in os.listdir(src):
        if not f.startswith('drawing.'):
            shutil.copy2(os.path.join(src, f), dst)
    try:
        make_drawings.process(u)
    except Exception as e:
        res.append(dict(uuid=u, error=str(e)[:80])); continue
    r = dict(uuid=u)
    for ext in ('dxf', 'svg'):
        a, b = os.path.join(src, 'drawing.' + ext), os.path.join(dst, 'drawing.' + ext)
        r[ext + '_bytes_equal'] = os.path.isfile(b) and sha(a) == sha(b)
    ea, eb = dxf_entities(os.path.join(src, 'drawing.dxf')), dxf_entities(os.path.join(dst, 'drawing.dxf'))
    r['dxf_entities_equal'] = ea == eb
    r['dxf_entities'] = [len(ea), len(eb)]
    res.append(r)
    print(r, flush=True)
shutil.rmtree(tmp, ignore_errors=True)
ok = [r for r in res if 'error' not in r]
summary = dict(n=len(res), errors=len(res) - len(ok),
               dxf_bytes_equal=sum(r['dxf_bytes_equal'] for r in ok),
               svg_bytes_equal=sum(r['svg_bytes_equal'] for r in ok),
               dxf_entities_equal=sum(r['dxf_entities_equal'] for r in ok))
json.dump(dict(summary=summary, records=res), open(os.path.join(ROOT, '_review', 'exp_aa_drawing_determinism.json'), 'w'), indent=1)
print(json.dumps(summary))
