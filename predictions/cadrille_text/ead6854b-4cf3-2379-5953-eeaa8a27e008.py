import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-25,99),(-24,99)).segment((-24,100)).close().assemble().reset().face(w0.sketch().segment((24,-100),(25,-99)).segment((24,-99)).close().assemble()).finalize().extrude(-200)