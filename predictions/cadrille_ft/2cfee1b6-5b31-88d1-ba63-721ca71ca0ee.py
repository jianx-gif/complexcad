import cadquery as cq
w0=cq.Workplane('XY').w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.workplane(offset=-50/2).cylinder(50,100).union(w1.sketch().circle(90).circle(37,mode='s').finalize().extrude(4))