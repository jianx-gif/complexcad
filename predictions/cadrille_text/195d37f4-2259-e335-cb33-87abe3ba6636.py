import cadquery as cq
w0=cq.Workplane('XY',origin=(-37,-27,-100))
w1=cq.Workplane('XY',origin=(-37,-27,-100))
r=w0.sketch().segment((26,-58),(37,-58)).segment((37,-48)).arc((32,-53),(26,-58)).assemble().finalize().extrude(200).union(w1.workplane(offset=190/2).moveTo(0,27).cylinder(190,2))