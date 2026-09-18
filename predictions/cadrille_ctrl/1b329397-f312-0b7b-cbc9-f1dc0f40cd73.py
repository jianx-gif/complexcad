import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-32,2),(-29,-15)).segment((-27,-15)).segment((-29,3)).arc((-30,2),(-32,2)).assemble().finalize().extrude(-10).union(w0.sketch().segment((-29,14),(-27,14)).segment((-27,16)).segment((-29,16)).close().assemble().finalize().extrude(-10)).union(w0.sketch().segment((-28,15),(-27,15)).segment((-27,14)).arc((-26,15),(-28,15)).assemble().push([(10,-1)]).circle(23).finalize().extrude(-10))
