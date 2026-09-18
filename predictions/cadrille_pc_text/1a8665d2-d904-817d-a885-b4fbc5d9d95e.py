import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-88,-10),(86,-35)).segment((88,10)).segment((-86,35)).close().assemble(),mode='s').finalize().extrude(-44)