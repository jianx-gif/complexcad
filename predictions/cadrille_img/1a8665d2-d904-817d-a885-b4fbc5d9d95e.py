import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-32,0))
w1=cq.Workplane('ZX',origin=(0,-31,0))
r=w0.sketch().circle(100).push([(19,26)]).circle(57,mode='s').circle(39).finalize().extrude(65).union(w1.sketch().push([(1,1)]).circle(89).push([(1,0)]).circle(53,mode='s').finalize().extrude(62))