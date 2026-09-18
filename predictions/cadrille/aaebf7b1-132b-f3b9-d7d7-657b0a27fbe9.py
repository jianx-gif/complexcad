import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
w1=cq.Workplane('YZ',origin=(65,0,0))
r=w0.workplane(offset=-13/2).box(190,190,13).union(w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(98)).union(w1.sketch().push([(-3,0)]).circle(68).circle(62,mode='s').finalize().extrude(-140))