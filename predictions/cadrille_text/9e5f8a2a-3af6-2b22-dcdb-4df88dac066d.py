import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-10))
w1=cq.Workplane('XY',origin=(-100,-1,-10))
r=w0.sketch().circle(4).circle(3,mode='s').finalize().extrude(20).union(w1.sketch().segment((-48,19),(-48,28)).arc((-49,23),(-48,19)).assemble().finalize().extrude(20))