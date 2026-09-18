import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,48,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().segment((-24,-14),(-18,-25)).segment((24,14)).segment((18,25)).close().assemble().finalize().extrude(-96).union(w0.sketch().segment((-38,-30),(-28,-37)).segment((38,30)).segment((30,36)).close().assemble().finalize().extrude(-68)).union(w1.sketch().circle(7).circle(3,mode='s').finalize().extrude(-77))
