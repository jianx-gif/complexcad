# -*- coding: utf-8 -*-
"""受保护的 CadQuery 程序执行 (批量版): 一个子进程顺序执行一批程序, 每个程序单独 try/except 并逐条输出结果;
父进程监控子进程内存 (>mem_gb 杀) 与单批总时限; 被杀时该批未完成的程序逐个单独重跑 (再超限即判失败).
(2026-09-08 事故: 一个预测程序让 OCC 吞掉 56 GB 虚拟内存, 耗尽系统提交内存, 拖垮了 GPU 训练.)
用法: from guarded_exec import run_guarded_batch
      results = run_guarded_batch([(key, code), ...], fn_mod, fn_name, mem_gb=3, per_item_timeout=60)
      -> {key: (ok, payload_or_reason)}
"""
import os, sys, time, subprocess, json, tempfile, base64
import psutil

WORKER = r'''
import sys, json, math, base64, traceback
import cadquery as cq
from types import SimpleNamespace
sys.path.insert(0, r'E:/3005/data/_review')
fn_mod, fn_name = sys.argv[1], sys.argv[2]
mod = __import__(fn_mod); fn = getattr(mod, fn_name)
batch = json.load(open(sys.argv[3], encoding='utf-8'))
for key, b64 in batch:
    code = base64.b64decode(b64).decode('utf-8')
    try:
        g = {'cq': cq, 'SimpleNamespace': SimpleNamespace, 'math': math, '__name__': '__cqx__'}
        exec(code, g)
        res = g.get('result')
        if res is None:
            for v in g.values():
                if isinstance(v, cq.Workplane):
                    res = v
        if res is None:
            raise RuntimeError('no shape')
        s = res.val() if hasattr(res, 'val') else res
        shape = s.wrapped if hasattr(s, 'wrapped') else s
        out = fn(shape)
        print('@@R@@' + json.dumps([key, True, out]), flush=True)
    except BaseException as e:
        print('@@R@@' + json.dumps([key, False, type(e).__name__ + ': ' + str(e)[:80]]), flush=True)
print('@@END@@', flush=True)
'''
PY = r'E:/anzhuang/Miniconda3/envs/cadquery/python.exe'
_ENVROOT = os.path.dirname(PY)
# 子进程要能从任何父环境启动: conda 环境的 DLL 目录必须在 PATH 里 (否则 python.exe 直接退出 127)
_CHILD_ENV = dict(os.environ)
_CHILD_ENV['PATH'] = os.pathsep.join([_ENVROOT, os.path.join(_ENVROOT, 'Library', 'mingw-w64', 'bin'), os.path.join(_ENVROOT, 'Library', 'usr', 'bin'),
                                      os.path.join(_ENVROOT, 'Library', 'bin'), os.path.join(_ENVROOT, 'Scripts'), os.path.join(_ENVROOT, 'bin'),
                                      os.environ.get('PATH', '')])
_CHILD_ENV['CONDA_PREFIX'] = _ENVROOT


def _run_batch(items, fn_mod, fn_name, mem_gb, timeout):
    """执行一批; 返回 (results dict, killed_reason or None, keys_done)."""
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(WORKER); wpath = f.name
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump([(k, base64.b64encode(c.encode('utf-8')).decode('ascii')) for k, c in items], f); bpath = f.name
    p = subprocess.Popen([PY, '-X', 'utf8', wpath, fn_mod, fn_name, bpath], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, encoding='utf-8', errors='replace', bufsize=1, env=_CHILD_ENV)
    results, reason = {}, None
    ps = psutil.Process(p.pid); t0 = time.time(); last = time.time()
    import threading
    lines = []

    def reader():
        for line in p.stdout:
            lines.append(line)
    th = threading.Thread(target=reader, daemon=True); th.start()
    consumed = 0
    try:
        while True:
            while consumed < len(lines):
                line = lines[consumed]; consumed += 1
                if line.startswith('@@R@@'):
                    key, ok, payload = json.loads(line[5:]); results[key] = (ok, payload); last = time.time()
                elif line.startswith('@@END@@'):
                    reason = None
            if p.poll() is not None and not th.is_alive():
                break
            try:
                if ps.memory_info().rss / 2**30 > mem_gb:
                    reason = 'memory>%.1fGB' % mem_gb; p.kill(); break
            except psutil.Error:
                pass
            if time.time() - last > timeout:
                reason = 'timeout'; p.kill(); break
            time.sleep(0.1)
        th.join(timeout=5)
        while consumed < len(lines):
            line = lines[consumed]; consumed += 1
            if line.startswith('@@R@@'):
                key, ok, payload = json.loads(line[5:]); results[key] = (ok, payload)
    finally:
        for f in (wpath, bpath):
            try:
                os.remove(f)
            except OSError:
                pass
    return results, reason


def run_guarded_batch(items, fn_mod, fn_name, mem_gb=3.0, per_item_timeout=60, batch_size=10):
    out = {}
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        res, reason = _run_batch(chunk, fn_mod, fn_name, mem_gb, per_item_timeout)
        out.update(res)
        pending = [(k, c) for k, c in chunk if k not in res]
        if pending and reason:
            # 被杀: 出事的是第一个未完成项; 它单独重跑一次 (再超限即失败), 其余继续成批
            k0, c0 = pending[0]
            r1, reason1 = _run_batch([(k0, c0)], fn_mod, fn_name, mem_gb, per_item_timeout)
            out[k0] = r1.get(k0, (False, reason1 or reason))
            rest = pending[1:]
            if rest:
                out.update(run_guarded_batch(rest, fn_mod, fn_name, mem_gb, per_item_timeout, batch_size))
        elif pending:
            for k, _ in pending:
                out[k] = (False, 'no result')
    return out


def run_guarded(code, fn_mod, fn_name, mem_gb=3.0, timeout=90):
    return run_guarded_batch([('x', code)], fn_mod, fn_name, mem_gb, timeout, 1)['x']
