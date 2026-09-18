import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(100).circle(50,mode='s').finalize().extrude(-200).union(w0.workplane(offset=-170/2).box(144,40,170))