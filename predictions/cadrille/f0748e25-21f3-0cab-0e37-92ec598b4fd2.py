import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().segment((-50,50),(-39,50)).arc((-36,52),(-33,50)).segment((50,50)).arc((0,100),(-50,50)).assemble().finalize().extrude(-15).union(w1.sketch().push([(9.5,0)]).rect(21,200).push([(10,81)]).circle(6,mode='s').finalize().extrude(-100))