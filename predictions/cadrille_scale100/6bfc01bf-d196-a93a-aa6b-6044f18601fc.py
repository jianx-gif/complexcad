import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,7,0))
w1=cq.Workplane('ZX',origin=(0,-6,0))
r=w0.sketch().segment((33,-23),(80,-45)).segment((80,-38)).segment((61,-38)).segment((61,-29)).segment((80,-29)).segment((80,45)).segment((74,45)).segment((74,38)).segment((52,33)).segment((52,32)).segment((50,32)).close().assemble().push([(61,0)]).circle(17,mode='s').finalize().extrude(-14).union(w1.sketch().push([(13,-1)]).circle(17).circle(11,mode='s').finalize().extrude(11))