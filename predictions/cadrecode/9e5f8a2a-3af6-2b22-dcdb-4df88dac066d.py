import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().rect(200,200).reset().face(w0.sketch().segment((-21,-14),(-2,-25)).segment((21,14)).segment((2,25)).close().assemble(),mode='s').finalize().extrude(-12)