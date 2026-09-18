import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-100))
w1=cq.Workplane('XY',origin=(-100,-10,-100))
r=w0.sketch().face(w0.sketch().segment((96,-32),(100,-32)).segment((100,-27)).arc((98,-29),(96,-32)).assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(100,0)).segment((100,0),(100,10)).segment((100,10),(0,10)).segment((0,10),(0,0)).assemble()).finalize().extrude(100))