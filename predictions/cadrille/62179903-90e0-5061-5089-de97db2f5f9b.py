import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-40))
w1=cq.Workplane('XY',origin=(0,0,-45))
r=w0.sketch().segment((-30,-70),(30,-70)).segment((30,-47)).arc((57,0),(30,47)).segment((30,70)).segment((-30,70)).segment((-30,47)).arc((-57,0),(-30,-47)).close().assemble().push([(-1,14)]).circle(13,mode='s').finalize().extrude(85).union(w1.sketch().arc((-29,74),(10,-100),(29,77)).segment((29,100)).segment((-29,100)).close().assemble().finalize().extrude(12))