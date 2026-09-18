import cadquery as cq
w0=cq.Workplane('XY',origin=(-77,-47,-100))
r=w0.sketch().segment((-77,47),(-76,47)).segment((-77,48)).close().assemble().reset().face(w0.sketch().segment((-77,47),(77,47)).segment((77,48)).segment((76,48)).segment((76,47)).segment((75,47)).segment((75,48)).segment((-77,48)).close().assemble()).finalize().extrude(200)