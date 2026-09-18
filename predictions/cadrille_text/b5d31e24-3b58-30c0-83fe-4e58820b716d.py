import cadquery as cq
w0=cq.Workplane('XY',origin=(-49,-17,-100))
r=w0.sketch().segment((-46,17),(-46,18)).arc((-47,16),(-45,17)).close().assemble().finalize().extrude(200)