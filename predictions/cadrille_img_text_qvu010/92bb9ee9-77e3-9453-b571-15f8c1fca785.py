import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-87,0))
r=w0.sketch().segment((-48,-10),(-44,-18)).segment((48,10)).segment((44,18)).close().assemble().finalize().extrude(-10).union(w1.sketch().circle(100).circle(73,mode='s').finalize().extrude(145))