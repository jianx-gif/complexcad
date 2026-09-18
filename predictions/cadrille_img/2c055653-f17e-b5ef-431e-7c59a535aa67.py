import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().push([(11,11)]).circle(89).circle(82,mode='s').circle(17).finalize().extrude(-11).union(w1.sketch().push([(11,11)]).circle(89).push([(-41,74)]).circle(16,mode='s').push([(11,11)]).circle(20,mode='s').push([(78,-17)]).circle(17,mode='s').circle(10).finalize().extrude(121))