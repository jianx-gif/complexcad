import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().circle(44).circle(15,mode='s').finalize().extrude(-4).union(w0.sketch().circle(44).circle(40,mode='s').finalize().extrude(20)).union(w1.sketch().circle(15).push([(-11,-1)]).circle(2,mode='s').finalize().extrude(-30))