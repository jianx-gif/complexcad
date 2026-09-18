import cadquery as cq
w0=cq.Workplane('XY',origin=(-11,0,-67))
r=w0.sketch().segment((28,-58),(36,-58)).segment((36,-52)).arc((32,-55),(28,-58)).assemble().finalize().extrude(134).union(w0.workplane(offset=134/2).moveTo(0,9).cylinder(134,3)).union(w0.workplane(offset=134/2).moveTo(0,9).cylinder(134,2))