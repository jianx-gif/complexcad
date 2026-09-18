import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(86).circle(2,mode='s').finalize().extrude(-194).union(w1.sketch().arc((-100,-24),(-96,-32),(-92,-40)).segment((-92,-50)).segment((-86,-50)).arc((0,-99),(86,-50)).segment((92,-50)).segment((92,-40)).arc((96,-32),(100,-24)).close().assemble().finalize().extrude(-153))