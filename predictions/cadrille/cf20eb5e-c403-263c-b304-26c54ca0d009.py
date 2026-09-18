import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.workplane(offset=139/2).box(4,186,139).union(w0.sketch().segment((-18,-100),(18,-100)).segment((18,-90)).segment((-3,-90)).segment((-3,90)).segment((18,90)).segment((18,100)).segment((-18,100)).close().assemble().finalize().extrude(150))