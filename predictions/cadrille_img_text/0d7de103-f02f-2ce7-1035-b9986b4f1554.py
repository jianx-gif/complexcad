import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-35,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-36,29),(-35,26),(-33,24)).arc((-29,26),(-25,27)).arc((-27,32),(-28,37)).arc((-32,33),(-36,29)).assemble().finalize().extrude(125).union(w1.sketch().arc((-95,-50),(0,-91),(95,-50)).segment((36,-50)).arc((0,-60),(-36,-50)).close().assemble().reset().face(w1.sketch().segment((-95,50),(-36,50)).arc((0,60),(36,50)).segment((95,50)).arc((0,91),(-95,50)).assemble()).finalize().extrude(200))