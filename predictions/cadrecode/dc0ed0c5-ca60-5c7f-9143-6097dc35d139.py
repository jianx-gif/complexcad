import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,96))
r=w0.sketch().segment((2,2),(2,3)).segment((3,3)).arc((-3,-4),(4,2)).close().assemble().finalize().extrude(-196).union(w0.sketch().push([(0,-1)]).circle(42).circle(31,mode='s').finalize().extrude(-134)).union(w0.sketch().circle(60).rect(26,58,mode='s').finalize().extrude(4))