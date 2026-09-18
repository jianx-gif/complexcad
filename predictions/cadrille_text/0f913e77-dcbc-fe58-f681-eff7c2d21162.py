import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,0,-100))
r=w0.sketch().segment((-47,19),(-47,22)).arc((-49,20),(-47,19)).assemble().finalize().extrude(200)