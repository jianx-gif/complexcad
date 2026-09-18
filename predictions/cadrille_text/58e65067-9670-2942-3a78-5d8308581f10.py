import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-53,-100))
r=w0.sketch().segment((-53,19),(-53,21)).segment((-51,21)).arc((-56,53),(-53,19)).assemble().finalize().extrude(200)