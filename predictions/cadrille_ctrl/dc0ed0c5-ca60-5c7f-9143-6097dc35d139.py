import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((7,-14),(6,-1),(14,-10)).arc((-10,11),(7,-14)).assemble().finalize().extrude(-200).union(w0.workplane(offset=-92/2).moveTo(1,0).cylinder(92,23)).union(w0.sketch().segment((-32,-1),(-27,-1)).arc((-26,-11),(-23,-20)).segment((-23,-21)).segment((9,-31)).segment((11,-28)).arc((24,-15),(27,1)).segment((32,-1)).segment((32,1)).segment((27,1)).arc((26,11),(23,20)).segment((23,21)).segment((-9,31)).segment((-11,28)).arc((-24,15),(-27,-1)).segment((-32,1)).close().assemble().finalize().extrude(-14))
