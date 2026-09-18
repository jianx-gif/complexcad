import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
w1=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(60).circle(40,mode='s').finalize().extrude(-50).union(w0.sketch().circle(100).circle(40,mode='s').finalize().extrude(150)).union(w1.sketch().segment((-12,-20),(12,-20)).segment((12,20)).segment((-12,20)).segment((-12,1)).arc((-10,-1),(-12,-3)).close().assemble().finalize().extrude(30))