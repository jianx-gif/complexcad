import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('XY',origin=(0,0,-62))
r=w0.sketch().segment((-3,-90),(3,-90)).segment((3,-87)).arc((0,-88),(-3,-87)).close().assemble().finalize().extrude(-44).union(w1.sketch().face(w1.sketch().push([(0,87)]).circle(3).push([(0,86.5)]).rect(4,3,mode='s').finalize().extrude(128))