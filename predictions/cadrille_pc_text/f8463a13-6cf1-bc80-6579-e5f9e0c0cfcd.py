import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,-11),(-67,-11)).arc((0,-68),(67,-11)).segment((84,-11)).segment((84,11)).segment((67,11)).arc((0,68),(-67,11)).segment((-84,11)).close().assemble(),mode='s').finalize().extrude(-200)