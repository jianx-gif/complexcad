import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-65))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-41,-59),(-33,-59)).arc((0,-68),(33,-59)).segment((39,-59)).segment((39,-55)).arc((68,0),(39,55)).segment((39,59)).segment((33,59)).arc((0,68),(-33,59)).segment((-41,59)).segment((-41,55)).arc((-68,0),(-41,-55)).close().assemble().finalize().extrude(165).union(w1.sketch().circle(47).circle(12,mode='s').finalize().extrude(190))