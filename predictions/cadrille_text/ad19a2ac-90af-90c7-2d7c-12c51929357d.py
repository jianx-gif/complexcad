import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
w1=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((29,-5),(29,133)).arc((11,11),(29,-5)).assemble().finalize().extrude(134).union(w1.sketch().face(w1.sketch().arc((92,-19),(100,11),(92,41)).close().assemble()).finalize().extrude(134))