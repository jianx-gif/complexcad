import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-35))
w1=cq.Workplane('ZX',origin=(0,-62,0))
r=w0.sketch().circle(19).circle(10,mode='s').finalize().extrude(71).union(w1.sketch().arc((-14,-98),(0,-98),(11,-94)).segment((11,94)).arc((0,98),(-11,98)).segment((-11,95)).segment((-14,95)).close().assemble().finalize().extrude(125))