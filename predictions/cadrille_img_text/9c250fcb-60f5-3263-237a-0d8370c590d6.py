import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().arc((-88,-49),(-87,-49),(-87,-50)).segment((-87,-46)).segment((-88,-46)).close().assemble().finalize().extrude(-199).union(w0.sketch().segment((-87,-34),(87,-34)).segment((87,-1)).arc((0,-33),(-87,-1)).close().assemble().finalize().extrude(-191)).union(w1.sketch().arc((-79,88),(-29,33),(-26,-40)).arc((18,46),(-79,88)).assemble().finalize().extrude(-119))