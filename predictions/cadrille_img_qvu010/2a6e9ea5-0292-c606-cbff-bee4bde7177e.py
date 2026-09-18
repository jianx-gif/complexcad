import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-95,0))
r=w0.sketch().circle(100).circle(97,mode='s').circle(70).finalize().extrude(109).union(w0.sketch().arc((-81,-1),(-79,-15),(-75,-29)).segment((-75,-66)).segment((-29,-66)).arc((0,-71),(29,-66)).segment((30,-66)).segment((30,-65)).arc((67,-35),(81,10)).segment((81,-1)).close().assemble().finalize().extrude(191))