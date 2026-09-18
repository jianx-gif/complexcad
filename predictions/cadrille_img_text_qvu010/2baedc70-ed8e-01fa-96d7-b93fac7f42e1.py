import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-76,0))
r=w0.sketch().arc((-100,16),(46,-89),(53,89)).segment((53,16)).close().assemble().push([(-10,0)]).circle(72,mode='s').finalize().extrude(29).union(w1.sketch().arc((-89,42),(-86,46),(-83,50)).arc((-82,54),(-78,55)).arc((-29,61),(13,38)).arc((19,40),(25,42)).arc((-32,68),(-89,42)).assemble().finalize().extrude(152))