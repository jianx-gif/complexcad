import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,71))
r=w0.sketch().arc((-74,66),(69,-72),(-67,74)).arc((-68,68),(-74,66)).assemble().push([(18,36)]).circle(53,mode='s').finalize().extrude(127).union(w1.workplane(offset=-162/2).moveTo(36,-1).cylinder(162,34))