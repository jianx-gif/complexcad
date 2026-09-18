import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,-13,0))
r=w0.sketch().circle(100).circle(96,mode='s').circle(30).finalize().extrude(-11).union(w1.sketch().arc((-100,20),(0,-81),(100,20)).segment((93,20)).arc((0,-80),(-93,20)).close().assemble().finalize().extrude(82))