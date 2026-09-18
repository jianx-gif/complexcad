import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((91,-40),(91,40)).arc((33,0),(91,-40)).assemble().finalize().extrude(100)