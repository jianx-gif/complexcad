import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().rect(200,200).reset().face(w0.sketch().segment((-19,-32),(19,-32)).segment((19,-12)).arc((22,0),(19,12)).segment((19,32)).segment((-19,32)).segment((-19,12)).arc((-22,0),(-19,-12)).close().assemble(),mode='s').finalize().extrude(-11)