import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-97))
w1=cq.Workplane('YZ',origin=(-6,0,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(194).union(w1.sketch().push([(0,1)]).circle(29).circle(25,mode='s').finalize().extrude(12))