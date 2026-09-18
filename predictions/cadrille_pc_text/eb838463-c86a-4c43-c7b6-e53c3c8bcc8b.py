import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(100).circle(70,mode='s').finalize().extrude(-16).union(w1.sketch().push([(0,1)]).circle(99).circle(34,mode='s').finalize().extrude(16))