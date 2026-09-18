import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(85).circle(65,mode='s').finalize().extrude(-40).union(w1.sketch().circle(75).circle(65,mode='s').finalize().extrude(-200))