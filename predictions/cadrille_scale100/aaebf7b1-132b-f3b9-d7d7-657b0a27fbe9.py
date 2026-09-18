import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('XY',origin=(0,0,53))
r=w0.workplane(offset=-5/2).box(76,76,5).union(w0.sketch().circle(40).circle(38,mode='s').finalize().extrude(37)).union(w1.sketch().circle(26).push([(-10,-4)]).circle(3,mode='s').finalize().extrude(-106))