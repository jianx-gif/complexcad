import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((91,-43),(100,-43)).segment((100,-23)).segment((91,-23)).arc((92,-33),(91,-43)).assemble().finalize().extrude(100)