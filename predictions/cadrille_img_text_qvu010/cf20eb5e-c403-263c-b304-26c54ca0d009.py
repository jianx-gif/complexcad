import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().segment((-100,-99),(100,-99)).segment((100,15)).segment((89,69)).segment((89,-15)).segment((10,-15)).arc((0,-16),(-10,-15)).segment((-100,-15)).close().assemble().finalize().extrude(65).union(w1.sketch().arc((-79,-28),(0,-81),(79,-28)).segment((67,-28)).arc((0,-72),(-67,-28)).close().assemble().finalize().extrude(-182))