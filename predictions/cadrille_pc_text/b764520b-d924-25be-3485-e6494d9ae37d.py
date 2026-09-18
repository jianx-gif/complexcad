import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(-38,0,0))
r=w0.sketch().push([(-56,0)]).circle(38).circle(32,mode='s').finalize().extrude(-100).union(w0.workplane(offset=100/2).moveTo(-56,0).cylinder(100,37)).union(w1.sketch().push([(0,-1)]).circle(25).circle(20,mode='s').finalize().extrude(132))