import cadquery as cq
w0=cq.Workplane('XY',origin=(-13,-13,-13))
r=w0.sketch().segment((11,-100),(13,-100)).segment((13,-3)).arc((12,-3),(11,-4)).close().assemble().finalize().extrude(27).union(w0.sketch().segment((-13,13),(13,13)).arc((0,18),(-13,13)).assemble().finalize().extrude(27))