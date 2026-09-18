import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
w1=cq.Workplane('XY',origin=(0,0,38))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(-77).union(w0.sketch().circle(85).circle(63,mode='s').finalize().extrude(-70)).union(w1.sketch().circle(85).circle(63,mode='s').finalize().extrude(14))