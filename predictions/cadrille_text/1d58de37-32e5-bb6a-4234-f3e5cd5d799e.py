import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-39),(100,-39)).segment((100,-33)).segment((93,-33)).arc((93,-36),(92,-39)).assemble().finalize().extrude(100).union(w0.sketch().push([(10,0)]).circle(50).circle(42,mode='s').finalize().extrude(100))