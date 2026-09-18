import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-25))
r=w0.sketch().segment((92,-39),(92,39)).arc((10,0),(92,-39)).assemble().finalize().extrude(50)