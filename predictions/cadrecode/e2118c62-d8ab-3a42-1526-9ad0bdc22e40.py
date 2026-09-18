import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,83))
r=w0.sketch().circle(100).rect(72,146,mode='s').finalize().extrude(-166).union(w0.sketch().circle(96).reset().face(w0.sketch().segment((-56,-7),(-48,-7)).arc((0,-50),(48,-7)).segment((56,-7)).segment((56,7)).segment((48,7)).arc((0,50),(-48,7)).segment((-56,7)).close().assemble(),mode='s').finalize().extrude(-147))