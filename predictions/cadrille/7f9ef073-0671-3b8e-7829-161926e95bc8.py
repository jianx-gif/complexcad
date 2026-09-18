import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,31))
w1=cq.Workplane('YZ',origin=(-41,0,0))
r=w0.sketch().segment((-100,-2),(-95,-2)).arc((0,-93),(95,-2)).segment((100,-2)).segment((100,2)).segment((95,2)).arc((0,93),(-95,2)).segment((-100,2)).close().assemble().reset().face(w0.sketch().segment((-48,-6),(-45,-6)).arc((0,-46),(45,-6)).segment((48,-6)).segment((48,6)).segment((45,6)).arc((0,47),(-45,6)).segment((-48,6)).close().assemble(),mode='s').finalize().extrude(-62).union(w1.workplane(offset=66/2).moveTo(10,13.5).box(78,7,66))