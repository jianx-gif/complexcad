import cadquery as cq
w0=cq.Workplane('XY',origin=(-29,-29,-100))
r=w0.sketch().segment((-29,19),(29,19)).arc((0,34),(-29,19)).assemble().finalize().extrude(199).union(w0.sketch().segment((24,-58),(29,-58)).segment((29,-19)).arc((27,-17),(29,-16)).segment((29,58)).segment((24,58)).close().assemble().finalize().extrude(200))