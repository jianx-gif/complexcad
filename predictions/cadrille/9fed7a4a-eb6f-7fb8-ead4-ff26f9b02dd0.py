import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-84))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-76,-17),(-66,-17)).arc((0,-76),(66,-17)).segment((76,-17)).segment((76,17)).segment((66,17)).arc((0,76),(-66,17)).segment((-76,17)).close().assemble(),mode='s').finalize().extrude(168)