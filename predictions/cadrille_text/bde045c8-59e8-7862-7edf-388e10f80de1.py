import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-1))
r=w0.sketch().segment((-46,17),(-46,18)).arc((-47,16),(-45,17)).close().assemble().finalize().extrude(-13).union(w0.sketch().segment((92,-17),(92,-16)).arc((91,-17),(93,-17)).close().assemble().finalize().extrude(10))