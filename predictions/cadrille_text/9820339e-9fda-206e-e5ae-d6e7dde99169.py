import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-40),(100,-40)).segment((100,-29)).segment((94,-29)).arc((94,-35),(92,-40)).assemble().finalize().extrude(100).union(w0.sketch().push([(100,0)]).circle(50).circle(4,mode='s').finalize().extrude(100))