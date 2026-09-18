import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().circle(100).circle(48,mode='s').finalize().extrude(-29).union(w0.sketch().arc((1,-78),(10,-77),(18,-78)).arc((-10,77),(1,-78)).assemble().finalize().extrude(105))