# -*- coding: utf-8 -*-
"""实验P (闭环) 数据准备: cadrille 在 ComplexCAD 上的微调训练集, 直接取自发布的划分文件.
训练池 = splits/train.txt (已执行成功、不在 400 件测试集、已剔除与测试件几何近重复者, 见 make_splits.py);
验证池 = splits/val_100.txt. 程序文件 <= MAX_CODE 字节 (覆盖约 94%); 去注释与 1500 字符上限在 exp_p_strip.py.
不复制文件: pkl 里放绝对路径. 输出 _review/cc_full/{train_all,val}.pkl, 统计写 cc_full/prep_stats.json.
(2026-09-13 起的版本: 之前的版本自己算近重复; 现在近重复与划分统一由 make_splits.py 产生, 本脚本只读它.)
"""
import os, json, pickle

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
DST = os.path.join(ROOT, '_review', 'cc_full')
MAX_CODE = 2400
os.makedirs(DST, exist_ok=True)


def read(name):
    return [l.strip() for l in open(os.path.join(ROOT, 'splits', name), encoding='utf-8') if l.strip()]


train_pool, val_pool = read('train.txt'), read('val_100.txt')
stats = dict(train_pool=len(train_pool), val_pool=len(val_pool), max_code_bytes=MAX_CODE)
for split, pool in (('train_all', train_pool), ('val', val_pool)):
    keep = []
    for u in pool:
        d = os.path.join(OUT, u)
        if not all(os.path.isfile(os.path.join(d, f)) for f in ('cadquery.py', 'model.stl', 'point_cloud.npy')):
            continue
        if os.path.getsize(os.path.join(d, 'cadquery.py')) > MAX_CODE:
            continue
        keep.append(u)
    ann = [{'mesh_path': os.path.join(OUT, u, 'model.stl'), 'py_path': os.path.join(OUT, u, 'cadquery.py'), 'uuid': u} for u in keep]
    pickle.dump(ann, open(os.path.join(DST, f'{split}.pkl'), 'wb'))
    stats[split] = len(keep)
    stats[split + '_too_long'] = len(pool) - len(keep)
json.dump(stats, open(os.path.join(DST, 'prep_stats.json'), 'w'), indent=1)
print(json.dumps(stats, indent=1))
