import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-62,0))
w1=cq.Workplane('XY',origin=(0,0,-79))
r=w0.sketch().push([(8,8)]).circle(92).circle(6,mode='s').finalize().extrude(121).union(w0.sketch().arc((-69,72),(-78,-61),(51,-86)).arc((78,-71),(98,-48)).arc((99,-46),(100,-43)).arc((38,93),(-69,72)).assemble().finalize().extrude(162)).union(w1.sketch().push([(8,0)]).circle(92).circle(35,mode='s').finalize().extrude(151))