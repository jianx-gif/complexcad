import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,24,0))
w1=cq.Workplane('ZX',origin=(0,24,0))
r=w0.sketch().segment((-40,-1),(-23,-34)).segment((-19,-32)).segment((-35,1)).close().assemble().reset().face(w0.sketch().segment((-30,20),(-29,19)).segment((-29,20)).close().assemble()).push([(-10,27)]).circle(11).reset().face(w0.sketch().segment((-19,27),(-18,25)).segment((-16,26)).segment((-17,28)).close().assemble(),mode='s').finalize().extrude(-24).union(w0.sketch().segment((-39,1),(-34,-18)).segment((-26,-16)).segment((-31,3)).close().assemble().push([(-10,27)]).circle(11).finalize().extrude(-24)).union(w0.workplane(offset=-24/2).moveTo(-10,27).cylinder(24,11)).union(w1.sketch().push([(-10,27)]).circle(11).push([(-10,27.5)]).rect(10,11,mode='s').finalize().extrude(-2))
