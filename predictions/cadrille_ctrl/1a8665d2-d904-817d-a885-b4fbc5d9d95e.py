import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((37,-19),(42,-19)).arc((-45,5),(43,-17)).segment((43,-11)).segment((37,-11)).arc((-17,-2),(37,-13)).close().assemble().finalize().extrude(20)
