import cadquery as cq
w0=cq.Workplane('XY',origin=(-11,0,-100))
r=w0.sketch().segment((90,-18),(90,-15)).segment((92,-15)).arc((86,-12),(90,-18)).assemble().finalize().extrude(200)