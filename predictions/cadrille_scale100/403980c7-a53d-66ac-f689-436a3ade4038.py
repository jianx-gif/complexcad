import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
w1=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().circle(40).circle(37,mode='s').finalize().extrude(-22).union(w0.sketch().circle(39).circle(24,mode='s').finalize().extrude(8)).union(w1.workplane(offset=-10/2).cylinder(10,45))