import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,-10),(-67,-10)).arc((0,-64),(67,-10)).segment((84,-10)).segment((84,10)).segment((67,10)).arc((0,75),(-67,10)).segment((-84,10)).close().assemble(),mode='s').finalize().extrude(200)