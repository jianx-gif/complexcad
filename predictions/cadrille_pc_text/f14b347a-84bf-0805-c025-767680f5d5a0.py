import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().segment((-50,-100),(50,-100)).segment((50,-75)).segment((11,-75)).arc((0,-86),(-11,-75)).segment((-25,-75)).segment((-25,100)).segment((-50,100)).segment((-50,-38)).arc((-45,-44),(-50,-50)).close().assemble().finalize().extrude(25)