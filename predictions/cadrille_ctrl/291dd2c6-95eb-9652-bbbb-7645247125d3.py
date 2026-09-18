import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().push([(10,0)]).circle(24).circle(21,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-34,-1),(-22,-1)).arc((-23,0),(-22,1)).segment((-34,1)).close().assemble().finalize().extrude(-8)).union(w0.sketch().push([(10,0)]).circle(24).circle(19,mode='s').finalize().extrude(-8))
