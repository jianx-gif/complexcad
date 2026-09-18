import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-40))
r=w0.sketch().segment((-30,-80),(30,-80)).segment((30,-15)).arc((36,10),(30,35)).segment((30,100)).segment((-30,100)).segment((-30,35)).arc((-36,10),(-30,-15)).close().assemble().push([(0,10)]).rect(30,6,mode='s').finalize().extrude(-5).union(w0.workplane(offset=85/2).moveTo(0,-10).cylinder(85,90))