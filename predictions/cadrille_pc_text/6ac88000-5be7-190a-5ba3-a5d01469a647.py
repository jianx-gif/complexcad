import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(80).circle(21,mode='s').finalize().extrude(32).union(w0.sketch().circle(61).circle(21,mode='s').finalize().extrude(56)).union(w1.sketch().arc((-87,49),(71,-70),(-50,88)).arc((-70,70),(-87,49)).assemble().push([(0,-1)]).circle(87,mode='s').finalize().extrude(16))