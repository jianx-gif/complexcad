import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().segment((-100,-50),(100,-50)).segment((100,50)).segment((83,50)).arc((55,46),(27,50)).segment((-100,50)).segment((-100,12)).arc((-97,-16),(-100,-43)).close().assemble().finalize().extrude(15).union(w0.workplane(offset=44/2).box(76,76,44))