import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().circle(40).reset().face(w0.sketch().segment((-28,-3),(-1,-28)).segment((28,3)).segment((1,28)).close().assemble(),mode='s').finalize().extrude(-8).union(w0.sketch().circle(15).circle(14,mode='s').finalize().extrude(-8))