import cadquery as cq
w0=cq.Workplane('YZ',origin=(59,0,0))
w1=cq.Workplane('ZX',origin=(0,66,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(41).union(w1.sketch().arc((-45,-86),(-10,-66),(1,-100)).arc((30,95),(-45,-86)).assemble().finalize().extrude(-158))