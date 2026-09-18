import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-74,-71),(21,-15),(65,82)).arc((11,-10),(-74,-71)).assemble().finalize().extrude(4).union(w0.sketch().segment((-63,-58),(-62,-58)).arc((-33,-26),(9,-14)).arc((35,33),(74,75)).arc((-11,33),(-63,-51)).close().assemble().finalize().extrude(200))