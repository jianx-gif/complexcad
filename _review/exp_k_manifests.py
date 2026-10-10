# -*- coding: utf-8 -*-
"""实验K: GrabCAD manifest (md5/大小/日期; URL/许可留待作者填) + 图纸审查包."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, glob, hashlib, csv, json, random, datetime

ROOT = _ROOT

# ---- 1) GrabCAD manifest ----
FIVE = ['Assem_Connecting_Rod_-_Connecting_Crank_', 'Assem_Connecting_Rod_-_Connecting_Rod_De',
        'Assem_Connecting_Rod_-_Rod_Bearing-1', 'Ball_Stud_throttle', 'C5_Knuckle_Mesh_Decimated']
rows = []
for f in sorted(glob.glob(os.path.join(ROOT, 'cadfit_repro', 'grabcad_run', '*.stl'))):
    name = os.path.splitext(os.path.basename(f))[0]
    h = hashlib.md5(open(f, 'rb').read()).hexdigest()
    st = os.stat(f)
    rows.append({'name': name,
                 'used_in_thesis_spot_check': name in FIVE,
                 'bytes': st.st_size, 'md5': h,
                 'file_date': datetime.date.fromtimestamp(st.st_mtime).isoformat(),
                 'source': 'grabcad.com/library (community model)',
                 'model_page_url': 'TODO(author)', 'licence': 'TODO(author)',
                 'processing': 'watertight repair; decimated where necessary'})
mpath = os.path.join(ROOT, '_review', 'grabcad_manifest.csv')
# NON-DESTRUCTIVE (2026-09-15): the released manifest carries author-entered provenance columns and the
# drawing-audit package carries reviewer sheets; never overwrite existing files, write *.regen.* instead.
if os.path.exists(mpath):
    mpath = mpath.replace('.csv', '.regen.csv')
with open(mpath, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print('manifest:', mpath, len(rows), 'files,', sum(r["used_in_thesis_spot_check"] for r in rows), 'in thesis')

# ---- 2) 图纸审查包 ----
random.seed(42)
metrics = [json.loads(l)['uuid'] for l in
           open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')]
have = [u for u in metrics if os.path.isfile(os.path.join(ROOT, 'output', u, 'drawing.png'))]
sample = random.sample(have, 200)
adir = os.path.join(ROOT, '_review', 'drawing_audit')
os.makedirs(adir, exist_ok=True)
with open(os.path.join(adir, 'checklist.regen.csv' if os.path.exists(os.path.join(adir, 'checklist.csv')) else 'checklist.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['idx', 'uuid', 'drawing_path',
                'views_correct', 'dims_correct', 'dims_missing', 'dims_duplicate_or_conflict',
                'text_line_collision', 'scale_titleblock_ok', 'reviewer', 'notes'])
    for i, u in enumerate(sample, 1):
        w.writerow([i, u, os.path.join('output', u, 'drawing.png'), '', '', '', '', '', '', '', ''])
open(os.path.join(adir, 'README.regen.md' if os.path.exists(os.path.join(adir, 'README.md')) else 'README.md'), 'w', encoding='utf-8').write(
"""# Drawing Audit Package (200 random drawings, seed=42)

按批注要求的双人审查协议:
1. 两名有制图经验的评审各自独立填写 checklist.csv(列: 视图正确/尺寸正确/漏标/重复冲突/
   文字压线/比例与标题栏), 取值 1=合格 0=不合格, notes 记录问题.
2. 双方填完后计算逐项一致率(Cohen's kappa 或简单一致百分比)并汇总错误率.
3. 结果填入论文 §Drawing 部分替换 'audit pending' 表述.
drawing_path 相对 <repo>/.
""")
print('audit package:', adir, len(sample), 'drawings listed')
