import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('ZX',origin=(0,5,0))
r=w0.sketch().circle(80).reset().face(w0.sketch().segment((-54,-10),(-1,-54)).segment((54,10)).segment((1,54)).close().assemble(),mode='s').finalize().extrude(-12).union(w0.sketch().circle(41).circle(37,mode='s').finalize().extrude(-2)).union(w1.sketch().segment((-20,-15),(20,-15)).segment((20,15)).segment((-1,15)).arc((-10,18),(-19,15)).segment((-20,15)).segment((-20,14)).arc((-21,9),(-20,4)).close().assemble().finalize().extrude(-5))
