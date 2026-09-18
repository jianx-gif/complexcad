import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,13,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().arc((-100,99),(40,35),(100,-99)).segment((100,99)).close().assemble().finalize().extrude(-29).union(w1.sketch().arc((-100,99),(29,35),(100,-99)).segment((100,99)).close().assemble().finalize().extrude(-76))