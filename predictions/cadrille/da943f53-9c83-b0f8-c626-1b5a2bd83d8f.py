import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,36))
w1=cq.Workplane('YZ',origin=(-46,0,0))
r=w0.workplane(offset=-87/2).cylinder(87,41).union(w0.workplane(offset=-56/2).cylinder(56,75)).union(w0.sketch().segment((-54,-86),(-47,-86)).arc((0,-99),(47,-86)).segment((54,-86)).segment((54,-82)).arc((99,-18),(81,59)).arc((63,71),(54,86)).segment((47,86)).arc((0,99),(-47,86)).segment((-54,86)).segment((-54,82)).arc((-100,0),(-54,-82)).close().assemble().finalize().extrude(-9)).union(w1.sketch().arc((-15,45),(1,-51),(15,45)).close().assemble().finalize().extrude(62))