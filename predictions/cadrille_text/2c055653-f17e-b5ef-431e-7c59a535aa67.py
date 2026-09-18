import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-33))
r=w0.sketch().segment((-100,17),(-99,17)).segment((-99,15)).segment((-96,15)).segment((-96,17)).segment((-95,17)).segment((-95,19)).segment((-96,19)).segment((-96,21)).segment((-99,21)).segment((-99,19)).segment((-100,19)).close().assemble().finalize().extrude(20).union(w0.workplane(offset=67/2).moveTo(0,17).cylinder(67,3))