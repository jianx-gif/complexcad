import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().segment((-100,-99),(-94,-99)).segment((68,-5)).segment((-94,99)).segment((-100,99)).close().assemble().finalize().extrude(26).union(w1.workplane(offset=66/2).moveTo(87,0).box(26,40,66))