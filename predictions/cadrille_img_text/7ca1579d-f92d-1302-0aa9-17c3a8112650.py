import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-27,0))
w1=cq.Workplane('YZ',origin=(89,0,0))
r=w0.sketch().segment((-77,67),(100,-49)).segment((100,-29)).segment((16,67)).close().assemble().finalize().extrude(10).union(w1.workplane(offset=-149/2).moveTo(-24,0).cylinder(149,4))