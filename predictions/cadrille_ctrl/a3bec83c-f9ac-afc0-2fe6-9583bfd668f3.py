import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-40,-18),(-31,-18)).segment((-31,-1)).segment((-40,-1)).close().assemble().finalize().extrude(-4).union(w0.sketch().segment((-39,-16),(-31,-16)).segment((-31,-11)).arc((-35,-13),(-39,-11)).close().assemble().reset().face(w0.sketch().arc((-39,-5),(-35,-3),(-31,-5)).segment((-31,1)).segment((-39,1)).close().assemble()).push([(17,0)]).circle(23).finalize().extrude(-4)).union(w0.sketch().segment((-2,-19),(39,-20)).segment((40,19)).segment((-1,20)).close().assemble().finalize().extrude(-4))
