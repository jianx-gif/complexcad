import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,65))
w1=cq.Workplane('YZ',origin=(53,0,0))
r=w0.sketch().circle(100).circle(40,mode='s').finalize().extrude(-145).union(w1.sketch().push([(0,40)]).circle(40).circle(32,mode='s').finalize().extrude(-98))