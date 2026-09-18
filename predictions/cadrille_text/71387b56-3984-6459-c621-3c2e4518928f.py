import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-17))
r=w0.sketch().segment((93,-17),(93,-14)).segment((96,-14)).arc((97,-13),(98,-14)).segment((99,-14)).arc((99,-12),(100,-11)).arc((99,-10),(99,-9)).arc((98,-9),(98,-8)).arc((98,-7),(99,-7)).arc((100,-5),(100,-3)).arc((99,-2),(99,-1)).arc((98,-1),(98,0)).arc((97,-1),(96,-1)).arc((96,-10),(93,-17)).assemble().finalize().extrude(34)