import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-70,-34),(-63,-46)).segment((70,34)).segment((63,46)).close().assemble(),mode='s').finalize().extrude(150)