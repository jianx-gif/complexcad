import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().arc((23,-19),(22,-16),(25,-17)).arc((-25,16),(23,-19)).assemble().circle(26,mode='s').finalize().extrude(-40).union(w0.sketch().segment((-33,-6),(-26,-6)).arc((-26,0),(-25,6)).segment((-33,6)).close().assemble().finalize().extrude(-39))
