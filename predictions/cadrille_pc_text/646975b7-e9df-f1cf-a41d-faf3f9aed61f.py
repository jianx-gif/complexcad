import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-58))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,1),(-79,1)).arc((0,-76),(79,1)).segment((84,1)).segment((84,17)).segment((79,17)).arc((0,77),(-79,17)).segment((-84,17)).close().assemble(),mode='s').finalize().extrude(117)