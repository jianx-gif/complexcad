import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,45,0))
w1=cq.Workplane('XY',origin=(0,0,44))
r=w0.sketch().arc((-65,-70),(28,-39),(41,61)).arc((17,-26),(-65,-70)).assemble().finalize().extrude(-145).union(w0.sketch().arc((-63,-69),(-25,11),(63,38)).arc((-68,59),(-63,-69)).assemble().finalize().extrude(55)).union(w1.sketch().arc((-45,79),(29,65),(94,19)).arc((42,95),(-45,79)).assemble().finalize().extrude(-36))