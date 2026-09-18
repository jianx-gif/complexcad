import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((29,-18),(29,18)).arc((17,0),(29,-18)).assemble().finalize().extrude(200)