import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-67))
r=w0.sketch().circle(100).reset().face(w0.sketch().arc((-84,-1),(0,-84),(84,-1)).segment((74,-1)).arc((0,-75),(-74,-1)).close().assemble(),mode='s').reset().face(w0.sketch().segment((-84,1),(-74,1)).arc((0,75),(74,1)).segment((84,1)).arc((0,84),(-84,1)).assemble(),mode='s').finalize().extrude(134)