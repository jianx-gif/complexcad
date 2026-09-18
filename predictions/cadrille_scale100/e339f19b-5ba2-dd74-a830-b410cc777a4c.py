import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-14,10),(-13,10)).segment((-13,11)).close().assemble().finalize().extrude(-80).union(w0.sketch().segment((-15,9),(-13,9)).segment((-13,10)).close().assemble().finalize().extrude(16)).union(w0.sketch().push([(0,-1)]).circle(14).circle(12,mode='s').finalize().extrude(80))