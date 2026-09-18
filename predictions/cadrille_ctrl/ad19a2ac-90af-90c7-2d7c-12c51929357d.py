import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().push([(0,-2)]).circle(28).circle(18,mode='s').finalize().extrude(-35).union(w0.sketch().push([(0,-2)]).circle(28).circle(22,mode='s').finalize().extrude(-35))
