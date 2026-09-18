import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('XY',origin=(0,0,-11))
r=w0.sketch().circle(88).circle(51,mode='s').finalize().extrude(-49).union(w0.sketch().circle(88).circle(48,mode='s').finalize().extrude(18)).union(w1.sketch().circle(100).push([(-1,87)]).circle(12,mode='s').finalize().extrude(-22))