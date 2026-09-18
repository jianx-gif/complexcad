import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((91,-41),(100,-41)).segment((100,-28)).segment((93,-28)).arc((93,-34),(91,-41)).assemble().finalize().extrude(100).union(w0.sketch().push([(55,0)]).circle(45).circle(44,mode='s').finalize().extrude(100))