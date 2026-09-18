import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-40),(100,-40)).segment((100,-28)).segment((94,-28)).arc((94,-34),(92,-40)).assemble().finalize().extrude(100).union(w0.sketch().push([(50,0)]).circle(50).circle(44,mode='s').finalize().extrude(100))