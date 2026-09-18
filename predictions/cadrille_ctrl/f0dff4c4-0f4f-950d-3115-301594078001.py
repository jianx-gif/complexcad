import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-29,-19),(-29,19)).arc((-35,0),(-29,-19)).assemble().reset().face(w0.sketch().arc((29,-19),(35,0),(29,19)).close().assemble()).finalize().extrude(-10).union(w0.sketch().circle(35).circle(15,mode='s').finalize().extrude(17)).union(w0.sketch().circle(35).circle(20,mode='s').finalize().extrude(20))
