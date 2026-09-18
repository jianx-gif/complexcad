import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((99,1),(100,6),(99,11)).close().assemble().finalize().extrude(-80).union(w0.sketch().push([(0,0)]).circle(30).circle(25,mode='s').finalize().extrude(80))
