import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().arc((-79,-54),(-1,-40),(79,-30)).segment((79,-26)).arc((1,-38),(-79,-54)).assemble().finalize().extrude(200).union(w1.sketch().arc((-54,-31),(-32,15),(-19,69)).arc((-35,18),(-54,-31)).assemble().finalize().extrude(155))