import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().segment((-100,-100),(100,-100)).segment((100,100)).segment((-100,100)).segment((-100,-93)).arc((-97,-95),(-100,-97)).close().assemble().finalize().extrude(100).union(w0.sketch().rect(100,100).rect(100,100,mode='s').finalize().extrude(100))