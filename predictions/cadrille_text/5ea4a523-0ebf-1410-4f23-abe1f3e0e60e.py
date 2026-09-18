import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-50,-100))
r=w0.sketch().segment((-50,50),(-48,50)).segment((-48,52)).close().assemble().finalize().extrude(200).union(w0.sketch().segment((48,-52),(50,-50)).segment((48,-50)).close().assemble().finalize().extrude(200))