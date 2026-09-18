import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().arc((-39,-8),(-35,-19),(-27,-29)).segment((-27,-18)).arc((-29,-13),(-27,-8)).segment((-27,24)).arc((-37,11),(-39,-5)).segment((-38,-5)).segment((-38,-8)).close().assemble().reset().face(w0.sketch().arc((-26,-30),(40,-4),(-22,31)).segment((-22,24)).arc((-20,13),(-22,1)).segment((-22,-30)).close().assemble()).reset().face(w0.sketch().arc((22,-18),(33,1),(22,24)).close().assemble(),mode='s').finalize().extrude(-8).union(w0.sketch().push([(0,-1)]).circle(39).circle(28,mode='s').finalize().extrude(-8))
