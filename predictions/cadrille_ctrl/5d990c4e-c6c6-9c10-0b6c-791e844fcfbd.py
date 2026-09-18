import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-27,-2),(-25,-2)).arc((-26,0),(-25,2)).segment((-27,2)).close().assemble().finalize().extrude(-80).union(w0.sketch().circle(25).circle(20,mode='s').finalize().extrude(80))
