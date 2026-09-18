import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,36))
r=w0.sketch().segment((-100,-19),(-99,-19)).segment((-99,-18)).close().assemble().reset().face(w0.sketch().segment((24,-58),(29,-58)).segment((29,-57)).close().assemble()).finalize().extrude(-93).union(w0.workplane(offset=-79/2).moveTo(0,1).cylinder(79,3)).union(w0.workplane(offset=64/2).moveTo(0,1).cylinder(64,3))