import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().segment((-52,0),(-51,-1)).segment((-51,0)).close().assemble().finalize().extrude(-61).union(w0.sketch().push([(0,0)]).circle(52).circle(30,mode='s').finalize().extrude(-8))