import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-30,6),(-27,6)).arc((-29,10),(-30,15)).close().assemble().finalize().extrude(-4).union(w0.sketch().push([(4,0)]).circle(26).circle(20,mode='s').finalize().extrude(14)).union(w0.sketch().push([(4,0)]).circle(25).circle(20,mode='s').finalize().extrude(35))