import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().segment((-40,5),(-22,5)).arc((-12,11),(-1,15)).segment((-1,20)).segment((1,20)).segment((1,15)).arc((12,11),(22,5)).segment((40,5)).arc((0,40),(-40,5)).assemble().finalize().extrude(-16).union(w0.sketch().push([(0,-1)]).circle(40).circle(20,mode='s').finalize().extrude(-14))