import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-58))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,1),(-81,1)).arc((0,-82),(81,1)).segment((84,1)).segment((84,4)).segment((81,4)).arc((0,82),(-81,4)).segment((-84,4)).close().assemble(),mode='s').finalize().extrude(117)