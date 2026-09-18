import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-50,-100),(50,-100)).segment((50,-75)).segment((12,-75)).arc((0,-86),(-12,-75)).segment((-25,-75)).segment((-25,100)).segment((-50,100)).segment((-50,-38)).arc((-45,-44),(-50,-50)).segment((-50,-85)).segment((-45,-85)).segment((-45,-98)).segment((-50,-98)).close().assemble().finalize().extrude(-24)