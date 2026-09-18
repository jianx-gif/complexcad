import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,87))
r=w0.sketch().segment((-100,-94),(100,-94)).segment((100,68)).segment((-71,94)).segment((-100,94)).close().assemble().circle(87,mode='s').finalize().extrude(65).union(w0.sketch().arc((-100,-10),(0,-100),(100,-10)).segment((89,-10)).arc((0,-89),(-89,-10)).close().assemble().finalize().extrude(125)).union(w1.sketch().arc((-48,-25),(0,-49),(48,-25)).segment((25,-25)).arc((0,-33),(-25,-25)).close().assemble().finalize().extrude(-175))