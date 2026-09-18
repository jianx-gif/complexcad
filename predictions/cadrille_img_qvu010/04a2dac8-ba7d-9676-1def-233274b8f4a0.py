import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-36,54),(-20,-79),(57,32)).arc((67,53),(58,74)).arc((-10,-93),(-10,92)).arc((-27,76),(-36,54)).assemble().finalize().extrude(-200).union(w0.sketch().circle(92).circle(85,mode='s').finalize().extrude(-192))