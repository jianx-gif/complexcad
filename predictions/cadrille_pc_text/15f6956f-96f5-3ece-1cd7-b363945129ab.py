import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((90,75)).segment((90,73)).segment((87,73)).segment((87,75)).segment((-100,75)).close().assemble().finalize().extrude(-10).union(w0.workplane(offset=5/2).cylinder(5,10))