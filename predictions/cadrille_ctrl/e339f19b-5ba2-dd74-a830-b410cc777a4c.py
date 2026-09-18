import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-14,9),(-13,9)).segment((-14,10)).close().assemble().finalize().extrude(-80).union(w0.sketch().segment((-15,7),(-13,7)).arc((0,-15),(13,7)).segment((15,7)).segment((15,10)).segment((13,10)).arc((0,15),(-13,10)).segment((-15,10)).close().assemble().push([(0,-4)]).circle(8,mode='s').finalize().extrude(80)).union(w0.sketch().push([(0,-1)]).circle(14).circle(12,mode='s').finalize().extrude(80))
