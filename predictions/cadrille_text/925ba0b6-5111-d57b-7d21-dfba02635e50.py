import cadquery as cq
w0=cq.Workplane('XY',origin=(-4,-41,-100))
r=w0.sketch().segment((27,-58),(46,-29)).segment((33,-29)).arc((31,-44),(27,-58)).assemble().finalize().extrude(190).union(w0.workplane(offset=200/2).moveTo(0,-4).cylinder(200,3))