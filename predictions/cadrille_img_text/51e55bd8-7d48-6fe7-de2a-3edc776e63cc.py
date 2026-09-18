import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-3))
w1=cq.Workplane('YZ',origin=(39,0,0))
r=w0.sketch().circle(100).circle(97,mode='s').finalize().extrude(84).union(w1.sketch().push([(0,1)]).circle(68).circle(54,mode='s').finalize().extrude(-77))