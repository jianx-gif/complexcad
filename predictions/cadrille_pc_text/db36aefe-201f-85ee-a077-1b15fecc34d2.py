import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,39))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(58).circle(13,mode='s').finalize().extrude(-78).union(w0.sketch().circle(100).circle(26,mode='s').finalize().extrude(-42)).union(w1.sketch().arc((52,-21),(39,0),(52,21)).arc((-52,0),(52,-21)).assemble().finalize().extrude(-187))