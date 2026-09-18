import cadquery as cq
w0=cq.Workplane('YZ',origin=(-99,0,0))
w1=cq.Workplane('XY',origin=(0,0,-59))
r=w0.sketch().arc((-69,-69),(67,74),(-62,-75)).segment((-59,-75)).arc((66,72),(-69,-66)).close().assemble().finalize().extrude(199).union(w1.sketch().arc((-99,-42),(-96,-43),(-94,-45)).arc((-95,-43),(-96,-41)).segment((-96,-42)).close().assemble().finalize().extrude(123))