import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-45,-1))
w1=cq.Workplane('XY',origin=(-100,-45,-1))
r=w0.sketch().circle(45).circle(35,mode='s').finalize().extrude(11).union(w1.sketch().segment((-5,-1),(-5,1)).segment((-2,1)).arc((-2,3),(0,3)).segment((0,4)).segment((2,4)).arc((4,4),(5,3)).segment((5,1)).segment((8,1)).segment((8,-1)).segment((5,-1)).arc((4,-3),(2,-3)).segment((0,-3)).segment((0,-1)).close().assemble().finalize().extrude(101))