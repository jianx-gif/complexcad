import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
w1=cq.Workplane('XY',origin=(0,0,-35))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((-100,62)).segment((-100,24)).arc((-76,-10),(-100,-44)).close().assemble().finalize().extrude(-20).union(w1.sketch().segment((-45,-37),(-30,-37)).segment((-30,37)).segment((-45,37)).segment((-45,22)).segment((-43,22)).segment((-43,18)).segment((-45,18)).close().assemble().finalize().extrude(70))