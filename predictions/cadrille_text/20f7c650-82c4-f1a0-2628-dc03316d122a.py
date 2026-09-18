import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-1))
w1=cq.Workplane('XY',origin=(-100,-1,-1))
r=w0.sketch().circle(10).circle(9,mode='s').finalize().extrude(101).union(w1.sketch().segment((29,-3),(29,3)).segment((30,3)).arc((-30,0),(30,-3)).close().assemble().finalize().extrude(-9))