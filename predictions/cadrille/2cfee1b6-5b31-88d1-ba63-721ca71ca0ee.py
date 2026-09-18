import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(78,0,0))
r=w0.workplane(offset=-50/2).cylinder(50,100).union(w1.sketch().circle(50).circle(46,mode='s').finalize().extrude(-158))