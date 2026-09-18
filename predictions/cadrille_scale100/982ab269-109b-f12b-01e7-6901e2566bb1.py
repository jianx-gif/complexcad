import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,58))
r=w0.sketch().segment((-32,-3),(-30,-3)).arc((0,-30),(30,-3)).segment((32,-3)).segment((32,3)).segment((30,3)).arc((0,30),(-30,3)).segment((-32,3)).close().assemble().finalize().extrude(0).union(w0.sketch().circle(32).circle(30,mode='s').finalize().extrude(70)).union(w1.sketch().circle(47).circle(11,mode='s').finalize().extrude(14))