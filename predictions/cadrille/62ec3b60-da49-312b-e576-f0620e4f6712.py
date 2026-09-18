import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,37))
r=w0.workplane(offset=-74/2).cylinder(74,100).union(w0.sketch().segment((-33,-90),(33,-90)).segment((33,-44)).arc((56,0),(33,44)).segment((33,90)).segment((-33,90)).segment((-33,44)).arc((-56,0),(-33,-44)).close().assemble().finalize().extrude(-5))