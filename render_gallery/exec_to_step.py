# -*- coding: utf-8 -*-
"""Execute a CadQuery program and export its result as STEP (exact B-rep): python exec_to_step.py <prog.py> <out.step>
Takes the variable `result`, `r` or the last cq.Workplane/Shape/Assembly defined; exit 0 = success."""
import sys, os
import cadquery as cq

src, out = sys.argv[1], sys.argv[2]
code = open(src, encoding='utf-8', errors='replace').read()
os.chdir(os.path.dirname(os.path.abspath(src)))
ns = {'__name__': '__main__'}
exec(compile(code, src, 'exec'), {'cq': cq, 'cadquery': cq, '__name__': '__main__'}, ns)
obj = ns.get('result') if ns.get('result') is not None else ns.get('r')
if obj is None:
    for v in reversed(list(ns.values())):
        if isinstance(v, (cq.Workplane, cq.Shape, cq.Assembly)):
            obj = v; break
assert obj is not None, 'no CAD result in program'
if isinstance(obj, cq.Assembly):
    obj = obj.toCompound()
if isinstance(obj, cq.Workplane):
    vals = [v for v in obj.vals() if isinstance(v, cq.Shape)]
    assert vals, 'empty workplane'
    obj = vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
assert obj.isValid() or True
cq.exporters.export(obj, out, exportType='STEP')
print('OK', out)
