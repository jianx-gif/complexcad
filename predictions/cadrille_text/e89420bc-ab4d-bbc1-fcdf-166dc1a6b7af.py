import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(200).union(w1.sketch().segment((-4,-90),(4,-90)).segment((4,-87)).arc((0,-88),(-4,-87)).close().assemble().finalize().extrude(190))