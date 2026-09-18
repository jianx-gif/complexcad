import cadquery as cq
w0=cq.Workplane('YZ',origin=(-38,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(25).circle(20,mode='s').finalize().extrude(132).union(w1.sketch().push([(-56,0)]).circle(38).circle(32,mode='s').finalize().extrude(-200))