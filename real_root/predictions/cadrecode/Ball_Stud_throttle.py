import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,-20))
r=w0.sketch().arc((-20,-4),(-10,-33),(19,-32)).arc((33,13),(-9,31)).segment((-9,33)).segment((-18,33)).segment((-18,28)).arc((-33,12),(-20,-4)).assemble().reset().face(w0.sketch().arc((-20,-4),(32,-17),(-18,10)).segment((-18,-4)).close().assemble(),mode='s').finalize().extrude(-189).union(w0.workplane(offset=-176/2).moveTo(0,0).cylinder(176,21)).union(w1.workplane(offset=49/2).moveTo(0,59).cylinder(49,41))