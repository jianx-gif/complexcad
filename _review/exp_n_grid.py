# -*- coding: utf-8 -*-
"""实验N: CAD-Recode 数值分布的精确、可复现分析 (AST 级, 全量 v1.5 train + v1 val).
解析对象: 每个 Call 节点的位置/关键字实参中的数值表达式 (Constant 数字, 及只含 Constant 的
UnaryOp/BinOp 算术, 元组逐元素展开), 求值后得到 (方法名, 参数位置, 值). 变量名实参 (Name) 单独计数
(不求值). 注释/字符串/标识符中的数字不计 (AST 不含它们). 去重: 按源码 SHA-1 统计精确重复.
分类: integer / half-integer (2v 为整但 v 不整) / other. 程序级指标: 全部数值在 0.5 网格上的程序比例,
Wilson 95% CI (程序为独立单元). 输出 _review/exp_n_grid.json.
用法: python exp_n_grid.py [--limit N]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
_DS = _os.environ.get('CADRECODE_DATASETS') or _ROOT + '/datasets'  # CAD-Recode dataset copies, see README
import os, sys, ast, json, hashlib, math, subprocess, threading, time
from collections import Counter, defaultdict

REPO = _DS + '/cadrecode_v15_train'
VAL1 = _DS + '/cadrecode_val/val'
OUT = _ROOT + '/_review/exp_n_grid.json'
LIMIT = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None


def iter_blobs(repo_dir, subdir):
    ls = subprocess.run(['git', '-C', repo_dir, 'ls-tree', '-r', '-z', 'HEAD', '--', subdir], capture_output=True, check=True)
    entries = []
    for rec in ls.stdout.split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        if not path.endswith(b'.py'):
            continue
        entries.append((meta.split(b' ')[2], path.decode('utf-8', 'replace')))
    if LIMIT:
        entries = entries[:LIMIT]
    p = subprocess.Popen(['git', '-C', repo_dir, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1 << 20)

    def feeder():
        for sha, _ in entries:
            p.stdin.write(sha + b'\n')
        p.stdin.close()
    threading.Thread(target=feeder, daemon=True).start()
    out = p.stdout
    for sha, path in entries:
        header = out.readline(); parts = header.split()
        if len(parts) < 3 or parts[1] != b'blob':
            continue
        size = int(parts[2]); data = out.read(size); out.read(1)
        yield path, data.decode('utf-8', 'replace')
    p.wait()


def num_expr(node):
    """数值表达式求值 (只接受 Constant 数字与其 Unary/Binary 算术); 非数值表达式返回 None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = num_expr(node.operand)
        return None if v is None else (-v if isinstance(node.op, ast.USub) else v)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
        a, b = num_expr(node.left), num_expr(node.right)
        if a is None or b is None:
            return None
        try:
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b != 0 else None}[type(node.op)]
        except Exception:
            return None
    return None


def classify(v):
    if abs(v - round(v)) < 1e-9:
        return 'integer'
    if abs(2 * v - round(2 * v)) < 1e-9:
        return 'half'
    return 'other'


def analyse(code):
    tree = ast.parse(code)
    vals = []          # (method, argpos, value, is_expr)
    n_name_args = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        m = node.func.attr if isinstance(node.func, ast.Attribute) else (node.func.id if isinstance(node.func, ast.Name) else '?')
        args = [(i, a) for i, a in enumerate(node.args)] + [(k.arg, k.value) for k in node.keywords]
        for pos, a in args:
            items = list(a.elts) if isinstance(a, (ast.Tuple, ast.List)) else [a]
            for it in items:
                if isinstance(it, ast.Name):
                    n_name_args += 1; continue
                if isinstance(it, ast.Call):
                    continue                       # 嵌套调用由 walk 单独处理
                v = num_expr(it)
                if v is None:
                    if isinstance(it, (ast.Constant,)):
                        continue                   # 字符串常量 (选择器 'XY' 等)
                    continue
                vals.append((m, str(pos), v, not isinstance(it, ast.Constant)))
    return vals, n_name_args


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (c - h), 3), round(100 * (c + h), 3))


def run(items, label):
    t0 = time.time()
    val_cls = Counter(); expr_cls = Counter(); per_method = defaultdict(Counter)
    n_prog = 0; n_parse_fail = 0; n_all_grid = 0; n_all_int = 0; n_no_vals = 0; n_names = 0
    n_vals = 0; vmin = float('inf'); vmax = float('-inf'); hashes = Counter(); ex_other = []
    n_all_grid_unique = 0; seen = set()
    for path, code in items:
        n_prog += 1
        h = hashlib.sha1(code.encode('utf-8', 'replace')).hexdigest(); hashes[h] += 1
        try:
            vals, nn = analyse(code)
        except SyntaxError:
            n_parse_fail += 1; continue
        n_names += nn
        if not vals:
            n_no_vals += 1; continue
        cls = [classify(v) for _, _, v, _ in vals]
        for (m, pos, v, is_expr), c in zip(vals, cls):
            val_cls[c] += 1; per_method[m][c] += 1; n_vals += 1
            if is_expr:
                expr_cls[c] += 1
            vmin = min(vmin, v); vmax = max(vmax, v)
            if c == 'other' and len(ex_other) < 8:
                ex_other.append((path, m, pos, v))
        if all(c != 'other' for c in cls):
            n_all_grid += 1
            if h not in seen:
                n_all_grid_unique += 1
        if all(c == 'integer' for c in cls):
            n_all_int += 1
        seen.add(h)
        if n_prog % 100000 == 0:
            print('  %s %d programs, %.0fs' % (label, n_prog, time.time() - t0), flush=True)
    n_unique = len(hashes); n_dup = n_prog - n_unique
    n_eval = n_prog - n_parse_fail - n_no_vals
    res = dict(label=label, programs=n_prog, parse_failures=n_parse_fail, programs_without_numeric_args=n_no_vals,
               programs_evaluated=n_eval, unique_programs=n_unique, exact_duplicates=n_dup,
               numeric_values=n_vals, name_arguments=n_names,
               value_classes=dict(val_cls), value_class_pct={k: round(100 * v / n_vals, 3) for k, v in val_cls.items()},
               values_from_expressions=sum(expr_cls.values()), expression_classes=dict(expr_cls),
               value_range=[vmin, vmax],
               programs_all_on_half_grid=n_all_grid, pct_all_on_half_grid=round(100 * n_all_grid / n_eval, 3),
               ci95_all_on_half_grid=wilson(n_all_grid, n_eval),
               programs_all_integer=n_all_int, pct_all_integer=round(100 * n_all_int / n_eval, 3),
               ci95_all_integer=wilson(n_all_int, n_eval),
               unique_programs_all_on_half_grid=n_all_grid_unique,
               per_method={m: dict(c) for m, c in sorted(per_method.items(), key=lambda kv: -sum(kv[1].values()))[:14]},
               examples_other=ex_other, seconds=round(time.time() - t0, 1))
    print(json.dumps({k: v for k, v in res.items() if k not in ('per_method', 'examples_other')}, indent=1), flush=True)
    return res


def main():
    out = {}
    import glob
    val_files = sorted(glob.glob(os.path.join(VAL1, '*.py')))
    out['v1_val'] = run(((f, open(f, encoding='utf-8', errors='replace').read()) for f in val_files), 'CAD-Recode v1 val')
    out['v15_train'] = run(iter_blobs(REPO, 'train'), 'CAD-Recode v1.5 train')
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1)
    print('written', OUT)


if __name__ == '__main__':
    main()
