import cadquery as cq
w0=cq.Workplane('XY',origin=(-33,-33,-100))
r=w0.sketch().segment((-33,33),(-33,34)).arc((-33,33),(-31,33)).close().assemble().finalize().extrude(18).union(w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((33,-53),(37,-57)).segment((39,-57)).arc((-33,33),(36,-58)).segment((37,-58)).arc((33,-61),(28,-58)).close().assemble().finalize().extrude(200))