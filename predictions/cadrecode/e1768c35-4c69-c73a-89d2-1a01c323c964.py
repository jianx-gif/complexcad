import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,55))
w1=cq.Workplane('ZX',origin=(0,-43,0))
r=w0.sketch().segment((-100,59),(-94,48)).arc((14,46),(70,-43)).segment((91,-43)).segment((91,-40)).segment((72,-17)).arc((15,59),(-80,67)).segment((-81,69)).close().assemble().finalize().extrude(-110).union(w1.workplane(offset=-33/2).moveTo(1,75).cylinder(33,25))