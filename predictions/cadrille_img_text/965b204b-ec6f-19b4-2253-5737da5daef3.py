import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-27,0,0))
r=w0.sketch().arc((-76,-29),(-2,-51),(71,-29)).close().assemble().reset().face(w0.sketch().segment((-76,51),(71,51)).arc((-2,73),(-76,51)).assemble()).finalize().extrude(200).union(w1.sketch().arc((-49,-85),(-26,-65),(-10,-39)).arc((-33,-58),(-49,-85)).assemble().finalize().extrude(115))