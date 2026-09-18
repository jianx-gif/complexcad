import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-12,-12))
r=w0.sketch().segment((29,-12),(29,12)).arc((27,0),(29,-12)).assemble().finalize().extrude(-28).union(w0.sketch().segment((31,-7),(31,7)).arc((27,0),(31,-7)).assemble().finalize().extrude(49)).union(w0.workplane(offset=102/2).moveTo(0,-11.5).box(10,11,102))