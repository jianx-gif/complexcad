import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(75).circle(65,mode='s').finalize().extrude(-100).union(w0.sketch().circle(85).circle(13,mode='s').finalize().extrude(40)).union(w0.sketch().circle(75).circle(65,mode='s').finalize().extrude(100))