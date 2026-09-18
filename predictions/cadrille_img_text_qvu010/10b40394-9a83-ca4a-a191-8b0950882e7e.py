import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,57,0))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().arc((-99,17),(-91,22),(-83,26)).arc((-79,33),(-73,38)).arc((-65,51),(-54,62)).arc((-79,46),(-99,17)).assemble().reset().face(w0.sketch().arc((-26,62),(35,1),(-25,-62)).arc((99,1),(-26,62)).assemble()).finalize().extrude(-75).union(w1.sketch().segment((-60,85),(-44,85)).arc((-40,92),(-35,99)).segment((-60,99)).close().assemble().finalize().extrude(-183))