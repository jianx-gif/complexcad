import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('XY',origin=(0,0,-38))
r=w0.sketch().circle(92).circle(89,mode='s').finalize().extrude(197).union(w1.sketch().push([(0,-1)]).circle(99).reset().face(w1.sketch().segment((-45,-59),(-28,-59)).arc((0,-66),(28,-59)).segment((45,-59)).segment((45,-47)).arc((66,-1),(45,47)).segment((45,59)).segment((28,59)).arc((0,66),(-28,59)).segment((-45,59)).segment((-45,47)).arc((-66,-1),(-45,-47)).close().assemble(),mode='s').finalize().extrude(119))