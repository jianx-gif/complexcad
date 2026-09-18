import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,38))
r=w0.workplane(offset=-101/2).cylinder(101,25).union(w0.sketch().arc((-98,20),(89,-46),(-77,63)).arc((-92,44),(-98,20)).assemble().finalize().extrude(25))