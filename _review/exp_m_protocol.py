# -*- coding: utf-8 -*-
"""实验M: 第3章 first-hand 数据集分析的协议补全.
  (a) 版本标识 + 文件 SHA-256 (Zero-To-CAD parquet, DeepCAD split json + test h5, CAD-Recode git HEAD,
      Fusion360 r1.0.1.zip);
  (b) 每个数据集的解析路径与操作匹配规则 (从 stat_*.py 读出);
  (c) 解析失败样本计数;
  (d) 解析精度交叉核验: Zero-To-CAD 与 CAD-Recode 用 Python ast 独立解析 (仅计真正的方法调用,
      注释/字符串/变量名不计) 与发布的正则结果逐模型比较; 报告一致率、假阳/假阴计数与样本.
  (e) 导出 40 件人工核验样本 (程序全文 + 两种解析器的判定) 供人工抽检.
输出: _review/exp_m_protocol.json, _review/parser_audit/
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
_DS = _os.environ.get('CADRECODE_DATASETS') or _ROOT + '/datasets'  # CAD-Recode dataset copies, see README
import os, sys, re, json, glob, ast, hashlib, subprocess, random, io
from collections import Counter

ROOT = _ROOT
DS = _DS
SCRIPTS = os.path.join(ROOT, 'Dataset Distribution', 'scripts')
OUT = os.path.join(ROOT, '_review', 'exp_m_protocol.json')
AUDIT = os.path.join(ROOT, '_review', 'parser_audit')
os.makedirs(AUDIT, exist_ok=True)
sys.path.insert(0, SCRIPTS)
from stat_zero_to_cad import OP_PATTERNS, SKETCH_PATTERNS, analyze_code   # 发布的正则规则

COMPLEX = ['loft', 'revolve', 'sweep', 'chamfer', 'fillet']
# 复杂操作的 CadQuery 方法名 (AST 只认 Attribute 调用的名字)
AST_METHODS = {'extrude': {'extrude', 'twistExtrude', 'cutBlind', 'cutThruAll'},
               'revolve': {'revolve'}, 'loft': {'loft'}, 'sweep': {'sweep'},
               'chamfer': {'chamfer'}, 'fillet': {'fillet'}, 'shell': {'shell'},
               'boolean_union': {'union', 'combine'}, 'boolean_cut': {'cut', 'subtract'},
               'boolean_intersect': {'intersect'},
               'pattern': {'polarArray', 'rarray', 'mirror', 'eachpoint'}}
NAME2CAT = {m: c for c, ms in AST_METHODS.items() for m in ms}


def sha256(path, buf=1 << 24):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ast_ops(code):
    """返回 (Counter 类别->调用次数, 解析错误串或 None). 只计 obj.method(...) 形式的真实调用."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return None, 'SyntaxError: %s' % str(e)[:60]
    c = Counter()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            cat = NAME2CAT.get(node.func.attr)
            if cat:
                c[cat] += 1
    return c, None


def regex_ops(code):
    ops, _ = analyze_code(code)
    return Counter(ops)


def compare(models, label):
    """models: list of (id, code). 逐模型比较正则 presence vs AST presence (按类别)."""
    agree = Counter(); fp = Counter(); fn = Counter()
    fp_ex, fn_ex = {}, {}
    n_syntax = 0
    per_model_complex = [0, 0, 0]      # both, regex-only, ast-only  (任一复杂操作 presence)
    for mid, code in models:
        r = regex_ops(code)
        a, err = ast_ops(code)
        if a is None:
            n_syntax += 1
            continue
        for cat in AST_METHODS:
            rp, ap = r.get(cat, 0) > 0, a.get(cat, 0) > 0
            if rp == ap:
                agree[cat] += 1
            elif rp:
                fp[cat] += 1; fp_ex.setdefault(cat, []).append(mid) if len(fp_ex.get(cat, [])) < 5 else None
            else:
                fn[cat] += 1; fn_ex.setdefault(cat, []).append(mid) if len(fn_ex.get(cat, [])) < 5 else None
        rc = any(r.get(c, 0) > 0 for c in COMPLEX); ac = any(a.get(c, 0) > 0 for c in COMPLEX)
        if rc and ac:
            per_model_complex[0] += 1
        elif rc:
            per_model_complex[1] += 1
        elif ac:
            per_model_complex[2] += 1
    n = len(models) - n_syntax
    res = dict(label=label, n_models=len(models), n_ast_syntax_error=n_syntax, n_compared=n,
               per_category={cat: dict(agree=agree[cat], regex_only=fp[cat], ast_only=fn[cat],
                                       agreement_pct=round(100.0 * agree[cat] / n, 3) if n else None)
                             for cat in AST_METHODS},
               any_complex=dict(both=per_model_complex[0], regex_only=per_model_complex[1], ast_only=per_model_complex[2]),
               examples_regex_only=fp_ex, examples_ast_only=fn_ex)
    return res


def load_ztc():
    import pyarrow.parquet as pq
    files = sorted(glob.glob(os.path.join(DS, 'zero_to_cad_test', '*.parquet')))
    models, meta = [], dict(n_files=len(files), files=[])
    n_empty = 0
    for fi, fp_ in enumerate(files):
        meta['files'].append(dict(name=os.path.basename(fp_), bytes=os.path.getsize(fp_), sha256=sha256(fp_)))
        t = pq.read_table(fp_, columns=['cadquery_file'])
        col = t.column('cadquery_file').to_pylist()
        for i, code in enumerate(col):
            if isinstance(code, bytes):
                code = code.decode('utf-8', errors='ignore')
            if code is None or not str(code).strip():
                n_empty += 1
                continue
            models.append(('ztc_f%02d#%d' % (fi, i), str(code)))
    meta['n_rows_with_code'] = len(models); meta['n_rows_empty_code'] = n_empty
    return models, meta


def load_cadrecode(sample_n, seed=0):
    repo = os.path.join(DS, 'cadrecode_v15_train')
    head = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    date = subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%ci'], capture_output=True, text=True).stdout.strip()
    remote = subprocess.run(['git', '-C', repo, 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(['git', '-C', repo, 'ls-tree', '-r', '--name-only', 'HEAD', '--', 'train'],
                          capture_output=True, text=True).stdout.splitlines()
    pys = [p for p in tree if p.endswith('.py')]
    rnd = random.Random(seed); pick = sorted(rnd.sample(pys, min(sample_n, len(pys))))
    models = []
    for p in pick:
        code = open(os.path.join(repo, p), encoding='utf-8', errors='ignore').read()
        models.append((p, code))
    meta = dict(git_head=head, git_head_date=date, remote=remote, n_train_py_in_tree=len(pys),
                sample_n=len(models), sample_seed=seed)
    return models, meta


def deepcad_meta():
    split = os.path.join(DS, 'deepcad', 'train_val_test_split.json')
    ids = json.load(open(split))['test']
    h5dir = os.path.join(DS, 'deepcad', 'cad_vec')
    missing = 0; h = hashlib.sha256()
    for rel in ids:
        p = os.path.join(h5dir, rel + '.h5')
        if not os.path.exists(p):
            missing += 1; continue
        h.update(open(p, 'rb').read())
    return dict(split_json_sha256=sha256(split), n_test_ids=len(ids), n_test_h5_missing=missing,
                test_h5_concat_sha256=h.hexdigest())


def fusion_meta():
    z = os.path.join(DS, 'r1.0.1.zip')
    js = glob.glob(os.path.join(DS, 'fusion360_recon', 'json', '*.json'))
    return dict(zip=os.path.basename(z), zip_bytes=os.path.getsize(z), zip_sha256=sha256(z), n_json=len(js))


def main():
    out = {}
    print('[1] Zero-To-CAD parquet hashes + load ...', flush=True)
    ztc, ztc_meta = load_ztc()
    out['zero_to_cad'] = dict(hf_repo='ADSKAILab/Zero-To-CAD-1m', split='test', **ztc_meta)
    print('    rows with code', len(ztc), 'empty', ztc_meta['n_rows_empty_code'], flush=True)
    print('[2] Zero-To-CAD regex-vs-AST cross-check ...', flush=True)
    out['zero_to_cad']['cross_check'] = compare(ztc, 'Zero-To-CAD test (all rows with code)')
    # 复现发布数字: 正则 presence 的 any-complex 比例
    n_any = sum(1 for _, c in ztc if any(regex_ops(c).get(k, 0) > 0 for k in COMPLEX))
    n_any_ast = sum(1 for _, c in ztc if (ast_ops(c)[0] or Counter()) and any(ast_ops(c)[0].get(k, 0) > 0 for k in COMPLEX))
    out['zero_to_cad']['any_complex_pct'] = dict(regex=round(100.0 * n_any / 10000, 2), ast=round(100.0 * n_any_ast / 10000, 2),
                                                 denominator=10000)
    print('    any-complex regex %.2f%%  ast %.2f%%' % (100.0 * n_any / 10000, 100.0 * n_any_ast / 10000), flush=True)

    print('[3] CAD-Recode v1.5 git identity + 20000-sample cross-check ...', flush=True)
    cr, cr_meta = load_cadrecode(20000)
    out['cad_recode'] = dict(hf_repo='filapro/cad-recode-v1.5', split='train', **cr_meta)
    out['cad_recode']['cross_check'] = compare(cr, 'CAD-Recode v1.5 train (20000-sample)')
    voc = Counter()
    for _, code in cr:
        for node in ast.walk(ast.parse(code)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                voc[node.func.attr] += 1
    out['cad_recode']['ast_method_vocabulary_sample'] = dict(voc.most_common())

    print('[4] DeepCAD + Fusion360 identities ...', flush=True)
    out['deepcad'] = dict(source='github rundiwu/DeepCAD (Google-Drive data release)', split='test',
                          parser='h5 "vec" command-type column (structured; no text parsing)', **deepcad_meta())
    out['fusion360'] = dict(source='S3 reconstruction/r1.0.1/r1.0.1.zip', split='reconstruction (all)',
                            parser='json sequence[].type + entities[].type (structured; no text parsing)', **fusion_meta())

    out['rules'] = dict(op_patterns=OP_PATTERNS, sketch_patterns=SKETCH_PATTERNS, ast_methods={k: sorted(v) for k, v in AST_METHODS.items()},
                        complex_ops=COMPLEX,
                        presence_definition='a model counts once per category if >=1 match; coverage = models with >=1 complex op / all models')

    # [5] 人工核验样本: 40 件 = 30 Zero-To-CAD (含全部分歧样本优先) + 10 CAD-Recode
    print('[5] audit sample ...', flush=True)
    rnd = random.Random(1)
    cc = out['zero_to_cad']['cross_check']
    disagree = set(sum(cc['examples_regex_only'].values(), []) + sum(cc['examples_ast_only'].values(), []))
    zt_idx = {m[0]: m for m in ztc}
    picks = [zt_idx[i] for i in sorted(disagree) if i in zt_idx][:10]
    rest = [m for m in ztc if m[0] not in disagree]
    picks += rnd.sample(rest, 30 - len(picks))
    picks += rnd.sample(cr, 10)
    rows = []
    for k, (mid, code) in enumerate(picks):
        r = regex_ops(code); a, _ = ast_ops(code)
        fn = os.path.join(AUDIT, '%02d_%s.py' % (k, re.sub(r'[^A-Za-z0-9_.-]', '_', mid)[:40]))
        open(fn, 'w', encoding='utf-8').write(code)
        rows.append(dict(file=os.path.basename(fn), source=mid, regex={c: int(r.get(c, 0) > 0) for c in COMPLEX},
                         ast={c: int((a or Counter()).get(c, 0) > 0) for c in COMPLEX}, human={c: '' for c in COMPLEX}))
    with open(os.path.join(AUDIT, 'audit_sheet.csv'), 'w', encoding='utf-8', newline='') as f:
        f.write('file,source,' + ','.join('regex_' + c for c in COMPLEX) + ',' + ','.join('ast_' + c for c in COMPLEX) + ',' + ','.join('human_' + c for c in COMPLEX) + '\n')
        for r in rows:
            f.write(r['file'] + ',' + r['source'] + ',' + ','.join(str(r['regex'][c]) for c in COMPLEX) + ',' + ','.join(str(r['ast'][c]) for c in COMPLEX) + ',' + ','.join('' for c in COMPLEX) + '\n')
    open(os.path.join(AUDIT, 'README.md'), 'w', encoding='utf-8').write(
        '# Parser audit sample\n\n40 programs (30 Zero-To-CAD test, 10 CAD-Recode v1.5 train). For each file, mark in '
        'audit_sheet.csv (human_* columns) whether the program really calls loft/revolve/sweep/chamfer/fillet '
        '(1 = yes, 0 = no). The regex_* and ast_* columns are the two automatic parsers; disagreements between them '
        'are listed first. Human precision = agreement of human with the regex columns.\n')
    out['audit_sample'] = dict(dir=AUDIT, n=len(rows), n_disagreement_first=len(picks[:10]))
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out['zero_to_cad'].items() if k not in ('files',)}, indent=1)[:3000])
    print(json.dumps({k: v for k, v in out['cad_recode'].items() if k != 'ast_method_vocabulary_sample'}, indent=1)[:2000])
    print('deepcad', out['deepcad']); print('fusion', out['fusion360'])


if __name__ == '__main__':
    main()
