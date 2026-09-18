# -*- coding: utf-8 -*-
"""实验H数据准备: ComplexCAD 微调 pilot 集 (cadrille CadRecodeDataset 格式).
选 2000 训练件(不在400测试子集, 代码<=1200字符, 已执行成功) + 50 验证件;
复制 model.stl + cadquery.py -> _review/cc_ft/train|val/<uuid>.{stl,py}; 写 pkl.
"""
import os, json, glob, random, shutil, pickle

ROOT = r'E:/3005/data'
DST = os.path.join(ROOT, '_review', 'cc_ft')
MAX_CODE = 1200
N_TRAIN, N_VAL = 2000, 50

test = set(l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip())
ok_exec = set()
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    if j.get('status') == 'ok':
        ok_exec.add(j['uuid'])

cands = []
for d in glob.glob(os.path.join(ROOT, 'output', '*')):
    u = os.path.basename(d)
    if u in test or u not in ok_exec:
        continue
    py = os.path.join(d, 'cadquery.py')
    stl = os.path.join(d, 'model.stl')
    if not (os.path.isfile(py) and os.path.isfile(stl)):
        continue
    try:
        n = os.path.getsize(py)
    except OSError:
        continue
    if n <= MAX_CODE:
        cands.append(u)

random.seed(42)
random.shuffle(cands)
sel = cands[:N_TRAIN + N_VAL]
print('candidates(code<=%d):' % MAX_CODE, len(cands), '| selected:', len(sel))

for split, uuids in (('train', sel[:N_TRAIN]), ('val', sel[N_TRAIN:N_TRAIN + N_VAL])):
    sd = os.path.join(DST, split)
    os.makedirs(sd, exist_ok=True)
    ann = []
    for u in uuids:
        shutil.copyfile(os.path.join(ROOT, 'output', u, 'model.stl'), os.path.join(sd, u + '.stl'))
        shutil.copyfile(os.path.join(ROOT, 'output', u, 'cadquery.py'), os.path.join(sd, u + '.py'))
        ann.append({'mesh_path': f'{split}/{u}.stl', 'py_path': f'{split}/{u}.py'})
    with open(os.path.join(DST, f'{split}.pkl'), 'wb') as f:
        pickle.dump(ann, f)
    print(split, len(ann), 'files copied')
print('DONE ->', DST)
