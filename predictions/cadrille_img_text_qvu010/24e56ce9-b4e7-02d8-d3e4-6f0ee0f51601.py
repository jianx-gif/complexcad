import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,64,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-81,-11),(-54,-16),(-60,-42)).arc((71,46),(-81,-11)).assemble().push([(21,23)]).circle(26,mode='s').finalize().extrude(-152).union(w1.sketch().circle(95).circle(89,mode='s').finalize().extrude(-36))