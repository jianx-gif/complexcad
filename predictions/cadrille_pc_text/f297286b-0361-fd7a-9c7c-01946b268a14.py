import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-9))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-48,-13),(37,-49)).segment((48,-22)).segment((-37,14)).close().assemble(),mode='s').finalize().extrude(18)