import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,19),(-37,19)).arc((-46,23),(-53,19)).assemble().finalize().extrude(100).union(w0.sketch().segment((26,-58),(57,-19)).segment((26,-19)).close().assemble().finalize().extrude(190)).union(w0.workplane(offset=200/2).moveTo(0,1).cylinder(200,3))