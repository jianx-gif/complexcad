import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-27,-100))
r=w0.sketch().segment((-53,15),(-37,15)).arc((-45,19),(-53,15)).assemble().finalize().extrude(200)