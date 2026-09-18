import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((33,-2),(43,-2)).segment((43,2)).segment((33,2)).close().assemble().finalize().extrude(-29).union(w0.sketch().segment((-40,-15),(-26,-15)).arc((-33,-10),(-40,-15)).assemble().finalize().extrude(-9)).union(w0.sketch().segment((-39,14),(-38,14)).segment((-38,15)).segment((-39,15)).close().assemble().reset().face(w0.sketch().segment((-38,-15),(-37,-15)).segment((-37,-14)).segment((-38,-14)).segment((-38,-16)).segment((-39,-16)).close().assemble()).push([(28,0)]).circle(15).finalize().extrude(-8))
