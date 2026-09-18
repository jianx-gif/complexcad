import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-17))
r=w0.sketch().segment((93,-17),(93,-14)).segment((95,-14)).arc((97,-12),(99,-14)).segment((100,-14)).arc((97,-11),(93,-17)).assemble().finalize().extrude(-28).union(w0.sketch().segment((93,-17),(93,-14)).segment((95,-14)).arc((97,-16),(99,-14)).segment((99,-17)).close().assemble().finalize().extrude(117))