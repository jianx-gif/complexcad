import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-27,10),(-26,11)).segment((-27,11)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-27,10),(-26,10)).segment((-27,11)).close().assemble().reset().face(w0.sketch().segment((-25,10),(-24,10)).segment((-25,11)).close().assemble()).reset().face(w0.sketch().segment((14,-15),(24,-15)).segment((24,-11)).segment((14,-11)).close().assemble()).finalize().extrude(-12))
