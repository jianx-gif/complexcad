import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,15),(-53,19)).arc((-54,17),(-53,15)).assemble().finalize().extrude(200)