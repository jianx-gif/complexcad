import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((10,62)).arc((7,59),(4,62)).segment((-100,62)).close().assemble().reset().face(w0.sketch().segment((-50,-37),(-45,-37)).arc((-37,-45),(-28,-37)).segment((50,-38)).segment((50,37)).segment((-50,38)).close().assemble(),mode='s').finalize().extrude(20)