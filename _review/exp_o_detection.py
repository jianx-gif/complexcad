# -*- coding: utf-8 -*-
"""实验O: 操作检测定义的可复现性证据 (Zero-To-CAD test 10000 程序, AST 级).
回答审阅问题: 注释/字符串是否排除; 选择器链 (.edges('|Z').fillet) 如何识别; 封装函数与别名如何处理;
循环/条件内的调用; 动态调用 getattr. 输出 _review/exp_o_detection.json.
"""
import sys, os, ast, json
from collections import Counter
sys.path.insert(0, r'E:/3005/data/_review'); sys.argv = ['x']
import exp_m_protocol as M

OPS = {'loft', 'revolve', 'sweep', 'chamfer', 'fillet'}


def analyse(code):
    t = ast.parse(code)
    r = Counter()
    # 函数定义与其内部的复杂操作调用
    fdefs = {}
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            inner = [c for c in ast.walk(n) if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr in OPS]
            fdefs[n.name] = bool(inner)
    called = {n.func.id for n in ast.walk(t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)} | {n.func.attr for n in ast.walk(t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}   # 函数名调用 或 方法调用 obj.build()
    if fdefs:
        r['has_funcdef'] = 1
    wrappers = [f for f, has in fdefs.items() if has]
    if wrappers:
        r['op_inside_funcdef'] = 1
        if any(f in called for f in wrappers):
            r['wrapper_called'] = 1
        else:
            r['wrapper_never_called'] = 1
    # 顶层 (函数体外) 是否有复杂操作调用
    top_calls = []
    for n in ast.walk(t):
        pass
    # 逐 Call 分类: 接收者是否选择器链; 是否在循环/条件/函数内
    parents = {}
    for n in ast.walk(t):
        for c in ast.iter_child_nodes(n):
            parents[c] = n

    def inside(n, kinds):
        p = parents.get(n)
        while p is not None:
            if isinstance(p, kinds):
                return True
            p = parents.get(p)
        return False
    for n in ast.walk(t):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in OPS:
            r['op_calls'] += 1
            recv = n.func.value
            if isinstance(recv, ast.Call) and isinstance(recv.func, ast.Attribute) and recv.func.attr in ('edges', 'faces', 'vertices', 'wires', 'solids'):
                r['op_calls_on_selector'] += 1
            if inside(n, (ast.For, ast.While)):
                r['op_calls_in_loop'] += 1
            if inside(n, (ast.If,)):
                r['op_calls_in_if'] += 1
            if inside(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                r['op_calls_in_funcdef'] += 1
        # 别名: 属性访问但不是调用 (f = obj.fillet)
        if isinstance(n, ast.Attribute) and n.attr in OPS and not (isinstance(parents.get(n), ast.Call) and parents[n].func is n):
            r['alias_attribute_access'] += 1
        # 动态: getattr(obj, 'fillet')
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'getattr':
            if len(n.args) > 1 and isinstance(n.args[1], ast.Constant) and n.args[1].value in OPS:
                r['getattr_dynamic'] += 1
    # 注释/字符串中的操作词 (正则会匹配, AST 不会)
    import re, io, tokenize
    words_in_comments = 0
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING) and re.search(r'\b(loft|revolve|sweep|chamfer|fillet)\b', tok.string, re.I):
                words_in_comments += 1
    except Exception:
        pass
    if words_in_comments:
        r['op_word_in_comment_or_string'] = 1
    return r


def main():
    ztc, _ = M.load_ztc()
    agg = Counter(); n_prog = Counter()
    for mid, code in ztc:
        r = analyse(code)
        for k, v in r.items():
            agg[k] += v
            n_prog[k] += 1
    out = dict(programs=len(ztc), totals=dict(agg), programs_with=dict(n_prog))
    print(json.dumps(out, indent=1))
    json.dump(out, open(r'E:/3005/data/_review/exp_o_detection.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
