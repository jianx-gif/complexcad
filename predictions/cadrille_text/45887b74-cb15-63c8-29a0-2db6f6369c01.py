import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-50))
r=w0.sketch().segment((91,-43),(100,-43)).segment((100,-19)).segment((91,-19)).arc((92,-30),(91,-43)).assemble().finalize().extrude(100)