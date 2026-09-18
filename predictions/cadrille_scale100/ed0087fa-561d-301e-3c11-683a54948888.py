import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(37).reset().face(w0.sketch().segment((-38,-6),(-21,-6)).arc((0,-22),(21,-6)).segment((38,-6)).segment((38,6)).segment((21,6)).arc((0,22),(-21,6)).segment((-38,6)).close().assemble(),mode='s').finalize().extrude(-5).union(w0.sketch().circle(45).circle(15,mode='s').finalize().extrude(25))