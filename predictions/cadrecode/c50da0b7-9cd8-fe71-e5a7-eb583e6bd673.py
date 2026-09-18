import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,64))
r=w0.sketch().circle(11).circle(5,mode='s').finalize().extrude(-164).union(w0.sketch().circle(22).reset().face(w0.sketch().segment((-9,2),(-2,-9)).segment((9,-2)).segment((2,9)).close().assemble(),mode='s').finalize().extrude(36))