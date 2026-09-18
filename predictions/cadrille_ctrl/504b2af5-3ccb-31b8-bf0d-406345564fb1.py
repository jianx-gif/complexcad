import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-2/2).moveTo(10,0).cylinder(2,2).union(w0.sketch().segment((-40,-15),(-23,-15)).arc((-32,-10),(-40,-15)).assemble().reset().face(w0.sketch().arc((-22,15),(-21,16),(-20,15)).segment((-20,17)).segment((-22,17)).close().assemble()).push([(10,0)]).rect(60,30).finalize().extrude(6)).union(w0.sketch().segment((-39,14),(-38,14)).segment((-38,15)).close().assemble().reset().face(w0.sketch().segment((-28,11),(39,3)).segment((40,15)).segment((-28,15)).close().assemble()).finalize().extrude(21))
