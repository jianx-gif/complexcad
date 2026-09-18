import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-56,0))
w1=cq.Workplane('XY',origin=(0,0,-91))
r=w0.sketch().arc((-59,-59),(-47,-66),(-34,-70)).close().assemble().reset().face(w0.sketch().arc((-27,-70),(-11,-67),(4,-61)).close().assemble()).reset().face(w0.sketch().segment((-18,70),(18,59)).arc((3,67),(-18,70)).assemble()).finalize().extrude(135).union(w1.sketch().segment((-88,-11),(-79,-11)).arc((-52,-55),(-10,-83)).arc((-10,-81),(-9,-79)).arc((-63,-1),(-88,83)).close().assemble().finalize().extrude(191))