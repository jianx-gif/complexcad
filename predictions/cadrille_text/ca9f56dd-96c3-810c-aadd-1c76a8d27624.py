import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-40),(100,-40)).segment((100,-29)).segment((92,-29)).arc((93,-35),(92,-40)).assemble().finalize().extrude(100)