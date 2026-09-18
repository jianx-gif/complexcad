import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,21,0))
w1=cq.Workplane('ZX',origin=(0,51,0))
r=w0.sketch().arc((-21,1),(1,18),(26,28)).arc((34,39),(45,48)).arc((-48,68),(-21,1)).assemble().finalize().extrude(-92).union(w0.sketch().circle(100).reset().face(w0.sketch().segment((-95,48),(-12,-81)).segment((95,-4)).segment((12,95)).close().assemble(),mode='s').finalize().extrude(29)).union(w1.sketch().arc((-89,39),(-29,-6),(-7,-82)).arc((74,40),(-89,39)).assemble().finalize().extrude(-10))