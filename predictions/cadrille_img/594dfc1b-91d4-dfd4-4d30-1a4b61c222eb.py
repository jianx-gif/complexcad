import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-65,-43),(-51,-48),(-42,-59)).arc((55,68),(-65,-43)).assemble().finalize().extrude(-179).union(w0.sketch().circle(89).circle(79,mode='s').finalize().extrude(-179)).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-98))