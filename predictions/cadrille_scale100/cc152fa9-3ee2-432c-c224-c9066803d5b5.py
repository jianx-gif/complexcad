import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('ZX',origin=(0,5,0))
r=w0.sketch().circle(80).reset().face(w0.sketch().segment((-54,-1),(-1,-54)).segment((54,1)).segment((1,54)).close().assemble(),mode='s').finalize().extrude(-12).union(w0.sketch().circle(41).circle(30,mode='s').finalize().extrude(-2)).union(w1.sketch().segment((-20,-15),(20,-15)).segment((20,15)).segment((10,15)).segment((10,-2)).segment((-20,-2)).close().assemble().finalize().extrude(-5))