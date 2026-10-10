# -*- coding: utf-8 -*-
"""实验R (装配闭环) 数据准备: 融合装配体网格 -> 点云, 目标 = 紧凑的紧固件放置程序.
  * 来源: 1m_Convert/assemblies_slim (单紧固件栈, 1011) + two_part_assemblies_slim (两件, 695);
  * 目标程序 = assembly_cadquery.py 中 base 加载之后、result 之前的放置块 (两件装配含 partB 的刚体变换),
    固定前言 (import / _load_part / base / result) 在执行时由 exp_r_asm_eval.py 补回 -> 仍是可执行 CadQuery;
  * 划分: 按基础零件 uuid 分组 (同一零件的单紧固件/两件装配同组), 随机 100 组做测试, 其余训练 (去 >1500 字符);
  * 输入点云: 训练由 CadRecodeDataset 从 model.stl 采样 (与零件闭环同一约定 mm/100); 测试预采 8192 点存 npy.
输出: _review/cc_asm/{train,val}.pkl, code/<name>.py, test_pc/<name>.npy, test_names.txt, prep_stats.json
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, pickle, random, re
import numpy as np
ROOT = _ROOT
SRC = [os.path.join(ROOT, '1m_Convert', 'assemblies_slim'), os.path.join(ROOT, '1m_Convert', 'two_part_assemblies_slim')]
DST = os.path.join(ROOT, '_review', 'cc_asm')
os.makedirs(os.path.join(DST, 'code'), exist_ok=True); os.makedirs(os.path.join(DST, 'test_pc'), exist_ok=True)
random.seed(7)


def placement_block(script):
    """取 base 加载之后到 result 之前的行 (放置块)."""
    lines = script.split('\n')
    start = None
    for i, l in enumerate(lines):
        if re.match(r"^base\w* = _load_part\(", l):
            start = i + 1
    end = next(i for i, l in enumerate(lines) if l.startswith('result = '))
    block = [l for l in lines[start:end] if l.strip()]
    return '\n'.join(block) + '\n'


def base_uuids(name):
    # 单件: <uuid>__M5_socket__asm ; 两件: <uuid12>_<uuid12>__M4__two (两件名是截断 uuid 前 12 位)
    head = name.split('__')[0]
    return [h[:12] for h in head.split('_')]


items = []
for src in SRC:
    for name in sorted(os.listdir(src)):
        d = os.path.join(src, name)
        py = os.path.join(d, 'assembly_cadquery.py'); stl = os.path.join(d, 'model.stl')
        if not (os.path.isfile(py) and os.path.isfile(stl)):
            continue
        block = placement_block(open(py, encoding='utf-8').read())
        items.append(dict(name=name, kind='two' if name.endswith('__two') else 'single', stl=stl, py=py,
                          block=block, bases=base_uuids(name)))
print('assemblies found', len(items), 'single', sum(i['kind'] == 'single' for i in items), 'two', sum(i['kind'] == 'two' for i in items))

# 按基础零件分组 (并查集: 两件装配把两个零件连成一组)
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for it in items:
    r = find(it['bases'][0])
    for b in it['bases'][1:]:
        parent[find(b)] = r
groups = {}
for it in items:
    groups.setdefault(find(it['bases'][0]), []).append(it)
gkeys = sorted(groups); random.shuffle(gkeys)
# 测试组: 取到恰好 >= 100 个装配体 (单/两件混合), 其余训练
test, k = [], 0
while len(test) < 100:
    test += groups[gkeys[k]]; k += 1
train_all = [it for g in gkeys[k:] for it in groups[g]]
train = [it for it in train_all if len(it['block']) <= 1500]
val = train[-40:]; train = train[:-40]
print('test', len(test), 'train_all', len(train_all), 'train(<=1500)', len(train), 'val', len(val))


def write_split(lst, split):
    ann = []
    for it in lst:
        cp = os.path.join(DST, 'code', it['name'] + '.py')
        open(cp, 'w', encoding='utf-8', newline='\n').write(it['block'])
        ann.append({'mesh_path': it['stl'], 'py_path': cp, 'uuid': it['name'], 'py_path_original': it['py']})
    pickle.dump(ann, open(os.path.join(DST, split + '.pkl'), 'wb'))
write_split(train, 'train'); write_split(val, 'val')

# 测试点云: 8192 面积加权采样 (mm), 推理端再 FPS 到 n_points 并 /100
import trimesh
for it in test:
    m = trimesh.load(it['stl'], force='mesh')
    pts = np.asarray(trimesh.sample.sample_surface(m, 8192)[0], dtype=np.float32)
    np.save(os.path.join(DST, 'test_pc', it['name'] + '.npy'), pts)
    open(os.path.join(DST, 'code', it['name'] + '.py'), 'w', encoding='utf-8', newline='\n').write(it['block'])
open(os.path.join(DST, 'test_names.txt'), 'w').write('\n'.join(it['name'] for it in test))
json.dump(dict(n_items=len(items), n_test=len(test), test_single=sum(i['kind'] == 'single' for i in test),
               test_two=sum(i['kind'] == 'two' for i in test), n_train_all=len(train_all), n_train=len(train), n_val=len(val),
               block_chars_median=float(np.median([len(i['block']) for i in items])), seed=7),
          open(os.path.join(DST, 'prep_stats.json'), 'w'), indent=1)
print(open(os.path.join(DST, 'prep_stats.json')).read())
print('example block:\n' + test[0]['block'][:600])
