import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().rect(120,60).push([(-25,0)]).circle(5,mode='s').push([(42,-10)]).circle(12,mode='s').finalize().extrude(-12).union(w1.sketch().segment((62,-10),(100,-10)).segment((100,10)).segment((62,10)).arc((63,0),(62,-10)).assemble().finalize().extrude(-8))