import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-90,-90))
r=w0.sketch().segment((-97,83),(-96,83)).segment((-96,82)).arc((-94,85),(-97,83)).assemble().finalize().extrude(180).union(w0.sketch().segment((96,-16),(96,-14)).segment((97,-14)).arc((99,-12),(100,-10)).arc((99,-9),(99,-8)).arc((97,-10),(96,-12)).segment((96,-15)).close().assemble().finalize().extrude(180))