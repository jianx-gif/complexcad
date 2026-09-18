import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-19,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-100,-16),(-46,19),(14,35)).arc((-58,38),(-100,-16)).assemble().finalize().extrude(114).union(w1.sketch().arc((-95,10),(-46,18),(-4,3)).arc((1,10),(7,16)).segment((-3,16)).arc((1,22),(4,29)).segment((16,29)).arc((24,27),(32,29)).segment((35,29)).segment((35,31)).arc((42,46),(45,62)).segment((-63,62)).arc((-79,37),(-95,10)).assemble().finalize().extrude(200))