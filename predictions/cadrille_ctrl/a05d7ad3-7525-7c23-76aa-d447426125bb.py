import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-27,-30),(-27,-20)).arc((-39,0),(-27,20)).segment((-27,30)).arc((-40,0),(-27,-30)).assemble().reset().face(w0.sketch().arc((-25,-31),(40,0),(-25,31)).segment((-25,20)).arc((-13,0),(-25,-20)).close().assemble()).finalize().extrude(-5).union(w0.workplane(offset=2/2).moveTo(-1,0).cylinder(2,30))
