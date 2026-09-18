import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
w1=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().arc((-19,5),(18,-7),(-1,20)).arc((-10,12),(-19,5)).assemble().finalize().extrude(15).union(w1.workplane(offset=-80/2).moveTo(0,-1).cylinder(80,11))
