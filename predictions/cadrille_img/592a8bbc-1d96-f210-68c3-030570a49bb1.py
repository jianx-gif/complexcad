import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-21,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().segment((-100,-1),(-83,-1)).arc((0,-83),(83,-1)).segment((100,-1)).segment((100,1)).segment((83,1)).arc((0,83),(-83,1)).segment((-100,1)).close().assemble().finalize().extrude(78).union(w1.sketch().segment((14,-99),(14,-77)).arc((-78,0),(14,77)).segment((14,99)).arc((-100,0),(14,-99)).assemble().finalize().extrude(54))