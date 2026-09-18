import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,38))
w1=cq.Workplane('ZX',origin=(0,-37,0))
r=w0.sketch().circle(100).circle(63,mode='s').finalize().extrude(-113).union(w1.sketch().arc((25,-50),(38,-35),(55,-27)).segment((55,27)).arc((38,35),(25,50)).close().assemble().finalize().extrude(73))