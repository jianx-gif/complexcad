# -*- coding: utf-8 -*-
"""闭环训练目标预处理: 去掉训练程序中的注释与空行 (自然语言注释不可预测且与几何无关; 变量名与结构保留),
写到 cc_full/code/<uuid>.py; 然后只保留去注释后 <= MAX_CHARS 字符的样本 (12 GB 显存余量),
写 train.pkl / val.pkl (train_all.pkl 保留全部长度). 报告长度统计到 strip_stats.json."""
import os, io, pickle, tokenize, json
import numpy as np

DST = r'E:/3005/data/_review/cc_full'
CODE = os.path.join(DST, 'code'); os.makedirs(CODE, exist_ok=True)
MAX_CHARS = 1500


def strip_comments(src):
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except Exception:
        return src
    result = [tok for tok in toks if tok.type != tokenize.COMMENT]
    src2 = tokenize.untokenize(result)
    lines = [l.rstrip() for l in src2.splitlines()]
    lines = [l for l in lines if l.strip()]
    return '\n'.join(lines) + '\n'


stats = {}
for split, out_name in (('train_all', 'train'), ('val', 'val')):
    ann = pickle.load(open(os.path.join(DST, f'{split}.pkl'), 'rb'))
    before, after, kept = [], [], []
    for a in ann:
        src = open(a['py_path_original'] if 'py_path_original' in a else a['py_path'], encoding='utf-8').read()
        s2 = strip_comments(src)
        compile(s2, a['uuid'], 'exec')            # 必须仍可编译
        p2 = os.path.join(CODE, a['uuid'] + '.py')
        open(p2, 'w', encoding='utf-8', newline='\n').write(s2)
        a['py_path_original'] = a['py_path_original'] if 'py_path_original' in a else a['py_path']; a['py_path'] = p2
        before.append(len(src)); after.append(len(s2))
        if len(s2) <= MAX_CHARS:
            kept.append(a)
    pickle.dump(ann, open(os.path.join(DST, f'{split}.pkl'), 'wb'))
    pickle.dump(kept, open(os.path.join(DST, f'{out_name}.pkl'), 'wb'))
    open(os.path.join(DST, f'{out_name}_uuids.txt'), 'w').write('\n'.join(a['uuid'] for a in kept) + '\n')
    stats[out_name] = dict(n_all=len(ann), n=len(kept), max_chars=MAX_CHARS, chars_before=int(np.mean(before)),
                           chars_after=int(np.mean(after)), max_after=int(max(len(open(a['py_path'], encoding='utf-8').read()) for a in kept)))
    print(out_name, stats[out_name], flush=True)
json.dump(stats, open(os.path.join(DST, 'strip_stats.json'), 'w'), indent=1)
